"""MLflow experiment tracking for AEGIE research runs."""

import os
from typing import Any, Dict, Optional

import mlflow


DEFAULT_TRACKING_URI = os.getenv(
    "AEGIE_MLFLOW_TRACKING_URI",
    "http://127.0.0.1:5003",
)

EXPERIMENT_NAME = os.getenv(
    "AEGIE_MLFLOW_EXPERIMENT",
    "AEGIE_Interview_Evaluation",
)


def configure_mlflow() -> None:
    """Configure the MLflow tracking server and experiment."""
    mlflow.set_tracking_uri(DEFAULT_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)


def start_interview_run(
    participant_id: str,
    job_role: str,
    collection_mode: str,
):
    """Start one MLflow run for an AEGIE interview."""
    configure_mlflow()

    run = mlflow.start_run(
        run_name=f"{participant_id}_{job_role.replace(' ', '_')}"
    )

    mlflow.log_params(
        {
            "participant_id": participant_id,
            "job_role": job_role,
            "collection_mode": collection_mode,
            "framework": "AEGIE",
            "stt_engine": "parakeet-tdt-0.6b-v2-int8",
            "semantic_model": "MiniLM-ONNX",
        }
    )

    return run


def log_question_result(
    question_number: int,
    question_id: str,
    difficulty: str,
    features: Dict[str, Any],
    adaptive_evidence: Optional[float] = None,
    adaptive_decision: Optional[str] = None,
) -> None:
    """Log research evidence for one evaluated interview response."""

    prefix = f"q{question_number}"

    mlflow.log_params(
        {
            f"{prefix}_question_id": question_id,
            f"{prefix}_difficulty": difficulty,
        }
    )

    metric_map = {
        "whole_similarity": "whole_similarity",
        "sentence_mean_similarity": "sentence_mean_similarity",
        "sentence_max_similarity": "sentence_max_similarity",
        "sentence_min_similarity": "sentence_min_similarity",
        "concept_mean_best_similarity": "concept_mean_best_similarity",
        "concept_max_best_similarity": "concept_max_best_similarity",
        "concept_min_best_similarity": "concept_min_best_similarity",
        "duration_sec": "duration_sec",
        "word_count": "word_count",
        "wpm": "wpm",
        "filler_count": "filler_count",
        "pause_count": "pause_count",
    }

    for source_key, metric_name in metric_map.items():
        value = features.get(source_key)

        if value is None:
            continue

        try:
            mlflow.log_metric(
                f"{prefix}_{metric_name}",
                float(value),
            )
        except (TypeError, ValueError):
            pass

    if adaptive_evidence is not None:
        mlflow.log_metric(
            f"{prefix}_adaptive_evidence",
            float(adaptive_evidence),
        )

    if adaptive_decision:
        mlflow.set_tag(
            f"{prefix}_adaptive_decision",
            str(adaptive_decision),
        )


def finish_interview_run(
    status: str = "FINISHED",
) -> None:
    """Finish the currently active AEGIE MLflow run."""
    active_run = mlflow.active_run()

    if active_run is None:
        return

    mlflow.set_tag("aegie_run_status", status)
    mlflow.end_run()