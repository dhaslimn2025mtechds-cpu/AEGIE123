# ============================================================
# AEGIE AGENT ARCHITECTURE
# ============================================================
#
# AEGIE:
# Adaptive Agentic AI-Based Voice Interview Evaluation
#
# Agents:
#
# 1. Interview Agent
# 2. Evaluation Agent
# 3. Adaptive Decision Agent
# 4. Feedback & Reporting Agent
#
# Research rule:
#
# Semantic and speech measurements are research FEATURES.
# They are NOT automatically converted into 1-5 scores.
#
# Human annotation labels are NOT used by the current
# DEVELOPMENT evidence pipeline.
#
# The legacy calibrated-scoring path remains independently
# gated. If no compatible frozen model exists, AEGIE keeps
# aegie_scores = None and does not fabricate scores.
#
# Development reference knowledge requires expert review
# before final research use.
#
# ============================================================


# ============================================================
# PACKAGE-SAFE IMPORTS
# ============================================================

try:

    from .question_selector import (
        select_question
    )

    from .semantic_evaluator import (
        prepare_semantic_evaluation
    )

    from .evaluation_features import (
        build_evaluation_features
    )

    from .calibrated_scorer import (
        generate_calibrated_scores,
        calibrated_model_exists
    )

except ImportError:

    from question_selector import (
        select_question
    )

    from semantic_evaluator import (
        prepare_semantic_evaluation
    )

    from evaluation_features import (
        build_evaluation_features
    )

    from calibrated_scorer import (
        generate_calibrated_scores,
        calibrated_model_exists
    )


# ============================================================
# 1. INTERVIEW AGENT
# ============================================================

class InterviewAgent:

    def __init__(self):

        self.name = "Interview Agent"


    # ========================================================
    # PROCESS
    # ========================================================

    def process(
        self,
        state
    ):

        print()
        print(
            "[Interview Agent]"
        )

        # ----------------------------------------------------
        # Basic interview state
        # ----------------------------------------------------

        job_role = state.get(
            "job_role"
        )

        question_number = state.get(
            "question_number",
            1
        )

        asked_question_ids = state.get(
            "asked_question_ids",
            []
        )

        target_difficulty = state.get(
            "next_difficulty"
        )

        # ----------------------------------------------------
        # Existing question
        # ----------------------------------------------------

        existing_question = state.get(
            "current_question"
        )

        if existing_question:

            print(
                "Current question already available."
            )

            print(
                "Question ID:",
                existing_question.get(
                    "question_id"
                )
            )

            print(
                "Difficulty:",
                existing_question.get(
                    "difficulty"
                )
            )

            state[
                "interview_agent_status"
            ] = "QUESTION_READY"

            return state

        # ----------------------------------------------------
        # Select question
        # ----------------------------------------------------

        question = select_question(

            job_role=
                job_role,

            question_number=
                question_number,

            asked_question_ids=
                asked_question_ids,

            target_difficulty=
                target_difficulty
        )

        # ----------------------------------------------------
        # No question
        # ----------------------------------------------------

        if question is None:

            if (
                question_number > 1
                and target_difficulty is None
            ):

                print(
                    "Waiting for adaptive "
                    "difficulty decision."
                )

                state[
                    "interview_agent_status"
                ] = (
                    "WAITING_FOR_ADAPTIVE_DECISION"
                )

            else:

                print(
                    "No suitable unused "
                    "question available."
                )

                state[
                    "interview_agent_status"
                ] = (
                    "NO_QUESTION_AVAILABLE"
                )

            return state

        # ----------------------------------------------------
        # Store selected question
        # ----------------------------------------------------

        state[
            "current_question"
        ] = question

        state[
            "current_difficulty"
        ] = question.get(
            "difficulty"
        )

        state[
            "interview_agent_status"
        ] = "QUESTION_READY"

        print(
            "Question selected successfully."
        )

        print(
            "Question ID:",
            question.get(
                "question_id"
            )
        )

        print(
            "Difficulty:",
            question.get(
                "difficulty"
            )
        )

        print(
            "Question:",
            question.get(
                "question_text"
            )
        )

        return state
# ============================================================
# 2. EVALUATION AGENT
# ============================================================

class EvaluationAgent:

    def __init__(self):

        self.name = (
            "Evaluation Agent"
        )

    # ========================================================
    # CLEAR EVALUATION OUTPUT
    # ========================================================

    @staticmethod
    def _clear_evaluation_outputs(
        state
    ):

        state[
            "evaluation_context"
        ] = None

        state[
            "semantic_evidence"
        ] = None

        state[
            "evaluation_features"
        ] = None

        state[
            "aegie_scores"
        ] = None

        state[
            "calibrated_scoring_status"
        ] = None

        state[
            "calibrated_scoring_reason"
        ] = None

    # ========================================================
    # PROCESS
    # ========================================================

    def process(
        self,
        state
    ):

        print()
        print(
            "[Evaluation Agent]"
        )

        # ----------------------------------------------------
        # Transcript required
        # ----------------------------------------------------

        transcript = state.get(
            "transcript"
        )

        if (
            transcript is None
            or not str(
                transcript
            ).strip()
        ):

            print(
                "Transcript is not available."
            )

            print(
                "Waiting for speech-to-text."
            )

            state[
                "evaluation_status"
            ] = "WAITING_FOR_TRANSCRIPT"

            self._clear_evaluation_outputs(
                state
            )

            return state

        # ----------------------------------------------------
        # Current question required
        # ----------------------------------------------------

        current_question = state.get(
            "current_question"
        )

        if not current_question:

            print(
                "Current question is not available."
            )

            state[
                "evaluation_status"
            ] = "WAITING_FOR_QUESTION"

            self._clear_evaluation_outputs(
                state
            )

            return state

        # ----------------------------------------------------
        # Question ID required
        # ----------------------------------------------------

        question_id = (
            current_question.get(
                "question_id"
            )
        )

        if not question_id:

            print(
                "Question ID is missing."
            )

            state[
                "evaluation_status"
            ] = "QUESTION_ID_MISSING"

            self._clear_evaluation_outputs(
                state
            )

            return state

        # ----------------------------------------------------
        # Generate complete semantic evidence
        #
        # This now uses:
        #
        # - Central 72-question registry
        # - Whole MiniLM evidence
        # - Sentence MiniLM evidence
        # - Concept Mean evidence
        #
        # No human score labels are used at runtime.
        # ----------------------------------------------------

        print(
            "Generating complete semantic "
            "evaluation evidence..."
        )

        try:

            semantic_result = (
                prepare_semantic_evaluation(
                    state,
                    generate_semantic_evidence=True
                )
            )

        except Exception as error:

            print(
                "Semantic evaluation failed."
            )

            print(
                "Reason:",
                str(error)
            )

            state[
                "evaluation_status"
            ] = (
                "SEMANTIC_EVALUATION_ERROR"
            )

            self._clear_evaluation_outputs(
                state
            )

            return state

        # ----------------------------------------------------
        # Semantic evaluation unsuccessful
        # ----------------------------------------------------

        if not semantic_result.get(
            "ready",
            False
        ):

            status = (
                semantic_result.get(
                    "status",
                    "SEMANTIC_EVALUATION_FAILED"
                )
            )

            reason = (
                semantic_result.get(
                    "reason"
                )
            )

            print(
                "Semantic evidence "
                "was not generated."
            )

            print(
                "Status:",
                status
            )

            print(
                "Reason:",
                reason
            )

            state[
                "evaluation_status"
            ] = status

            state[
                "evaluation_context"
            ] = semantic_result.get(
                "evaluation_context"
            )

            state[
                "semantic_evidence"
            ] = semantic_result.get(
                "semantic_evidence"
            )

            state[
                "evaluation_features"
            ] = None

            state[
                "aegie_scores"
            ] = None

            state[
                "calibrated_scoring_status"
            ] = None

            state[
                "calibrated_scoring_reason"
            ] = None

            return state

        # ----------------------------------------------------
        # Store semantic evaluation context
        # ----------------------------------------------------

        state[
            "evaluation_context"
        ] = semantic_result.get(
            "evaluation_context"
        )

        # ----------------------------------------------------
        # Store complete semantic evidence
        # ----------------------------------------------------

        semantic_evidence = (
            semantic_result.get(
                "semantic_evidence"
            )
        )

        state[
            "semantic_evidence"
        ] = semantic_evidence

        state[
            "evaluation_model"
        ] = (
            "sentence-transformers/"
            "all-MiniLM-L6-v2-ONNX"
        )

        print(
            "Semantic evidence generated."
        )

        print(
            "Question ID:",
            question_id
        )

        # ----------------------------------------------------
        # Reference role
        # ----------------------------------------------------

        reference_role = None

        if isinstance(
            semantic_evidence,
            dict
        ):

            reference_role = (
                semantic_evidence.get(
                    "reference_role"
                )
            )

        print(
            "Reference role:",
            reference_role
        )

        # ----------------------------------------------------
        # Whole MiniLM evidence
        # ----------------------------------------------------

        whole_answer = {}

        if isinstance(
            semantic_evidence,
            dict
        ):

            whole_answer = (
                semantic_evidence.get(
                    "whole_answer"
                )
                or {}
            )

        print()

        print(
            "Whole MiniLM evidence:"
        )

        print(
            "  Whole similarity:",
            whole_answer.get(
                "similarity"
            )
        )

        # ----------------------------------------------------
        # Sentence MiniLM evidence
        # ----------------------------------------------------

        sentence_level = {}

        if isinstance(
            semantic_evidence,
            dict
        ):

            sentence_level = (
                semantic_evidence.get(
                    "sentence_level"
                )
                or {}
            )

        print()

        print(
            "Sentence MiniLM evidence:"
        )

        print(
            "  Reference sentences:",
            sentence_level.get(
                "reference_sentence_count"
            )
        )

        print(
            "  Candidate sentences:",
            sentence_level.get(
                "candidate_sentence_count"
            )
        )

        print(
            "  Mean best similarity:",
            sentence_level.get(
                "mean_best_similarity"
            )
        )

        print(
            "  Maximum best similarity:",
            sentence_level.get(
                "max_best_similarity"
            )
        )

        print(
            "  Minimum best similarity:",
            sentence_level.get(
                "min_best_similarity"
            )
        )

        # ----------------------------------------------------
        # Concept Mean evidence
        # ----------------------------------------------------

        concept_level = {}

        if isinstance(
            semantic_evidence,
            dict
        ):

            concept_level = (
                semantic_evidence.get(
                    "concept_level"
                )
                or {}
            )

        print()

        print(
            "Concept Mean evidence:"
        )

        print(
            "  Reference concepts:",
            concept_level.get(
                "concept_count"
            )
        )

        print(
            "  Mean best similarity:",
            concept_level.get(
                "mean_best_similarity"
            )
        )

        print(
            "  Maximum best similarity:",
            concept_level.get(
                "max_best_similarity"
            )
        )

        print(
            "  Minimum best similarity:",
            concept_level.get(
                "min_best_similarity"
            )
        )

        # ----------------------------------------------------
        # Build combined evaluation feature vector
        # ----------------------------------------------------

        print()

        print(
            "Building combined evaluation "
            "feature vector..."
        )

        try:

            feature_result = (
                build_evaluation_features(
                    state
                )
            )

        except Exception as error:

            print(
                "Evaluation feature "
                "generation failed."
            )

            print(
                "Reason:",
                str(error)
            )

            state[
                "evaluation_status"
            ] = (
                "FEATURE_GENERATION_ERROR"
            )

            state[
                "evaluation_features"
            ] = None

            state[
                "aegie_scores"
            ] = None

            state[
                "calibrated_scoring_status"
            ] = None

            state[
                "calibrated_scoring_reason"
            ] = None

            return state

        # ----------------------------------------------------
        # Feature generation unsuccessful
        # ----------------------------------------------------

        if not feature_result.get(
            "success",
            False
        ):

            print(
                "Evaluation feature vector "
                "was not generated."
            )

            print(
                "Status:",
                feature_result.get(
                    "status"
                )
            )

            print(
                "Reason:",
                feature_result.get(
                    "reason"
                )
            )

            state[
                "evaluation_status"
            ] = feature_result.get(
                "status",
                "FEATURE_GENERATION_FAILED"
            )

            state[
                "evaluation_features"
            ] = None

            state[
                "aegie_scores"
            ] = None

            state[
                "calibrated_scoring_status"
            ] = None

            state[
                "calibrated_scoring_reason"
            ] = None

            return state

        # ----------------------------------------------------
        # Store combined feature vector
        # ----------------------------------------------------

        features = (
            feature_result.get(
                "features"
            )
        )

        state[
            "evaluation_features"
        ] = features

        # IMPORTANT:
        # Keep this status as EVALUATION_FEATURES_READY even if
        # calibrated scores are also generated later. app.py
        # uses this status to persist the feature record.

        state[
            "evaluation_status"
        ] = "EVALUATION_FEATURES_READY"

        print(
            "Evaluation feature vector generated."
        )

        # ----------------------------------------------------
        # Corrected three-part semantic features
        # ----------------------------------------------------

        print()

        print(
            "Whole MiniLM:",
            features.get(
                "whole_similarity"
            )
        )

        print(
            "Sentence MiniLM Mean:",
            features.get(
                "sentence_mean_best_similarity"
            )
        )

        print(
            "Sentence MiniLM Maximum:",
            features.get(
                "sentence_max_best_similarity"
            )
        )

        print(
            "Sentence MiniLM Minimum:",
            features.get(
                "sentence_min_best_similarity"
            )
        )

        print(
            "Concept Mean:",
            features.get(
                "concept_mean_best_similarity"
            )
        )

        print(
            "Concept Maximum:",
            features.get(
                "concept_max_best_similarity"
            )
        )

        print(
            "Concept Minimum:",
            features.get(
                "concept_min_best_similarity"
            )
        )

        print(
            "Reference Sentence Count:",
            features.get(
                "reference_sentence_count"
            )
        )

        print(
            "Reference Concept Count:",
            features.get(
                "reference_concept_count"
            )
        )

        print(
            "Answer Sentence Count:",
            features.get(
                "answer_sentence_count"
            )
        )

        # ----------------------------------------------------
        # Objective speech features
        # ----------------------------------------------------

        print()

        print(
            "Duration:",
            features.get(
                "duration_sec"
            )
        )

        print(
            "Word Count:",
            features.get(
                "word_count"
            )
        )

        print(
            "WPM:",
            features.get(
                "wpm"
            )
        )

        print(
            "Filler Count:",
            features.get(
                "filler_count"
            )
        )

        print(
            "Pause Count:",
            features.get(
                "pause_count"
            )
        )

        print(
            "Filler Rate / 100 Words:",
            features.get(
                "filler_rate_per_100_words"
            )
        )

        print(
            "Pause Rate / Minute:",
            features.get(
                "pause_rate_per_minute"
            )
        )

        # ----------------------------------------------------
        # CALIBRATED AEGIE SCORING
        #
        # IMPORTANT RESEARCH RULE:
        #
        # The feature vector is NEVER converted using arbitrary
        # hand-written thresholds.
        #
        # generate_calibrated_scores() returns scores only when
        # a compatible frozen calibrated model exists.
        #
        # Before calibration:
        #     aegie_scores = None
        #
        # After valid calibration:
        #     aegie_scores = five model predictions clipped
        #     to the approved 1-5 scale.
        # ----------------------------------------------------

        try:

            scoring_result = (
                generate_calibrated_scores(
                    features
                )
            )

        except Exception as error:

            scoring_result = {

                "success":
                    False,

                "status":
                    "CALIBRATED_SCORING_ERROR",

                "reason":
                    str(error),

                "scores":
                    None
            }

        state[
            "calibrated_scoring_status"
        ] = scoring_result.get(
            "status"
        )

        state[
            "calibrated_scoring_reason"
        ] = scoring_result.get(
            "reason"
        )

        print()

        print(
            "AEGIE 1-5 scores:"
        )

        if scoring_result.get(
            "success",
            False
        ):

            scores = scoring_result.get(
                "scores"
            )

            if isinstance(
                scores,
                dict
            ):

                state[
                    "aegie_scores"
                ] = scores

                print(
                    "Calibrated scores generated."
                )

                print(
                    "Relevance:",
                    scores.get(
                        "relevance_score"
                    )
                )

                print(
                    "Technical:",
                    scores.get(
                        "technical_score"
                    )
                )

                print(
                    "Clarity:",
                    scores.get(
                        "clarity_score"
                    )
                )

                print(
                    "Communication:",
                    scores.get(
                        "communication_score"
                    )
                )

                print(
                    "Overall:",
                    scores.get(
                        "overall_score"
                    )
                )

            else:

                state[
                    "aegie_scores"
                ] = None

                state[
                    "calibrated_scoring_status"
                ] = (
                    "CALIBRATED_SCORING_INVALID_OUTPUT"
                )

                state[
                    "calibrated_scoring_reason"
                ] = (
                    "Scoring result reported success "
                    "without a valid score dictionary."
                )

                print(
                    "Not generated - calibrated "
                    "scoring returned invalid output."
                )

        else:

            state[
                "aegie_scores"
            ] = None

            scoring_status = (
                scoring_result.get(
                    "status"
                )
            )

            if (
                scoring_status
                ==
                "CALIBRATION_MODEL_NOT_AVAILABLE"
            ):

                print(
                    "Not generated - "
                    "calibration pending."
                )

            else:

                print(
                    "Not generated - calibrated "
                    "scoring unavailable."
                )

                print(
                    "Status:",
                    scoring_status
                )

                reason = (
                    scoring_result.get(
                        "reason"
                    )
                )

                if reason:

                    print(
                        "Reason:",
                        reason
                    )

        return state
# ============================================================
# 3. ADAPTIVE DECISION AGENT
# ============================================================

class AdaptiveDecisionAgent:

    def __init__(self):

        self.name = (
            "Adaptive Decision Agent"
        )

    # ========================================================
    # DIFFICULTY MOVEMENT
    # ========================================================

    @staticmethod
    def _move_difficulty(
        current_difficulty,
        decision
    ):

        levels = [
            "Easy",
            "Medium",
            "Hard"
        ]

        if current_difficulty not in levels:
            return None

        current_index = levels.index(
            current_difficulty
        )

        if decision == "HARDER":

            new_index = min(
                current_index + 1,
                2
            )

        elif decision == "EASIER":

            new_index = max(
                current_index - 1,
                0
            )

        else:

            new_index = current_index

        return levels[
            new_index
        ]

    # ========================================================
    # PROCESS
    # ========================================================

    def process(
        self,
        state
    ):

        print()
        print(
            "[Adaptive Decision Agent]"
        )

        collection_mode = str(
            state.get(
                "collection_mode",
                "DEVELOPMENT"
            )
        ).strip().upper()

        features = state.get(
            "evaluation_features"
        )

        # ====================================================
        # DEVELOPMENT RULE-BASED PROTOTYPE
        # ====================================================

        if collection_mode == "DEVELOPMENT":

            if not isinstance(
                features,
                dict
            ):

                print(
                    "Evaluation features are not available."
                )

                state[
                    "adaptive_status"
                ] = "WAITING_FOR_EVALUATION"

                state[
                    "adaptive_evidence"
                ] = None

                state[
                    "adaptive_rule_decision"
                ] = None

                state[
                    "next_difficulty"
                ] = None

                return state

            semantic_evidence = state.get(
                "semantic_evidence"
            )

            if not isinstance(
                semantic_evidence,
                dict
            ):

                print(
                    "Semantic evidence is not available."
                )

                state[
                    "adaptive_status"
                ] = "WAITING_FOR_EVALUATION"

                state[
                    "adaptive_evidence"
                ] = None

                state[
                    "adaptive_rule_decision"
                ] = None

                state[
                    "next_difficulty"
                ] = None

                return state

            whole_answer = (
                semantic_evidence.get(
                    "whole_answer"
                )
                or {}
            )

            concept_level = (
                semantic_evidence.get(
                    "concept_level"
                )
                or {}
            )

            whole_similarity = (
                whole_answer.get(
                    "similarity"
                )
            )

            concept_mean = (
                concept_level.get(
                    "mean_best_similarity"
                )
            )

            try:

                whole_similarity = float(
                    whole_similarity
                )

                concept_mean = float(
                    concept_mean
                )

            except (
                TypeError,
                ValueError
            ):

                print(
                    "Required Whole MiniLM or Concept Mean "
                    "evidence is unavailable."
                )

                state[
                    "adaptive_status"
                ] = "WAITING_FOR_EVALUATION"

                state[
                    "adaptive_evidence"
                ] = None

                state[
                    "adaptive_rule_decision"
                ] = None

                state[
                    "next_difficulty"
                ] = None

                return state

            # =================================================
            # DEVELOPMENT RULE
            #
            # Adaptive Evidence =
            # 60% Concept Mean
            # + 40% Whole MiniLM
            #
            # Sentence MiniLM remains descriptive evidence and
            # does not determine technical question difficulty.
            #
            # Prototype thresholds only:
            # < 0.45       -> EASIER
            # 0.45 - <0.65 -> SAME
            # >= 0.65      -> HARDER
            #
            # Not validated competency scoring.
            # =================================================

            adaptive_evidence = (
                0.60 * concept_mean
                +
                0.40 * whole_similarity
            )

            if adaptive_evidence >= 0.65:

                decision = "HARDER"

            elif adaptive_evidence < 0.45:

                decision = "EASIER"

            else:

                decision = "SAME"

            current_difficulty = state.get(
                "current_difficulty"
            )

            next_difficulty = (
                self._move_difficulty(
                    current_difficulty,
                    decision
                )
            )

            state[
                "adaptive_evidence"
            ] = round(
                adaptive_evidence,
                4
            )

            state[
                "adaptive_rule_decision"
            ] = decision

            state[
                "next_difficulty"
            ] = next_difficulty

            state[
                "adaptive_status"
            ] = (
                "RULE_BASED_ADAPTATION_ACTIVE"
            )

            print(
                "Rule-based prototype adaptation active."
            )

            print(
                "Whole MiniLM:",
                round(
                    whole_similarity,
                    4
                )
            )

            print(
                "Concept Mean:",
                round(
                    concept_mean,
                    4
                )
            )

            print(
                "Adaptive evidence:",
                round(
                    adaptive_evidence,
                    4
                )
            )

            print(
                "Decision:",
                decision
            )

            print(
                "Current difficulty:",
                current_difficulty
            )

            print(
                "Next difficulty:",
                next_difficulty
            )

            print(
                "Prototype development thresholds only."
            )

            return state

        # ====================================================
        # PILOT / FINAL SAFEGUARD
        # ====================================================

        scores = state.get(
            "aegie_scores"
        )

        if scores is None:

            if features:

                state[
                    "adaptive_status"
                ] = (
                    "WAITING_FOR_CALIBRATED_EVALUATION"
                )

            else:

                state[
                    "adaptive_status"
                ] = (
                    "WAITING_FOR_EVALUATION"
                )

            state[
                "next_difficulty"
            ] = None

            return state

        state[
            "adaptive_status"
        ] = (
            "ADAPTATION_NOT_CALIBRATED"
        )

        state[
            "next_difficulty"
        ] = None

        return state
# ============================================================
# 4. FEEDBACK & REPORTING AGENT
# ============================================================

class FeedbackReportingAgent:

    def __init__(self):
        self.name = "Feedback & Reporting Agent"

    @staticmethod
    def _safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def process(self, state):

        print()
        print("[Feedback & Reporting Agent]")

        collection_mode = str(
            state.get("collection_mode", "DEVELOPMENT")
        ).strip().upper()

        features = state.get("evaluation_features")
        semantic_evidence = state.get("semantic_evidence")

        # ====================================================
        # DEVELOPMENT RULE-BASED PROTOTYPE
        #
        # Feedback Evidence =
        # 60% Concept Mean
        # + 40% Whole MiniLM
        #
        # Sentence MiniLM remains separate descriptive semantic
        # evidence. Speech measurements are descriptive only.
        #
        # No 1-5 score, pass/fail, or hiring decision is made.
        # ====================================================

        if collection_mode == "DEVELOPMENT":

            if not isinstance(features, dict):
                print("Evaluation features are not available.")
                state["feedback_status"] = "WAITING_FOR_EVALUATION"
                state["feedback"] = None
                return state

            if not isinstance(semantic_evidence, dict):
                print("Semantic evidence is not available.")
                state["feedback_status"] = "WAITING_FOR_EVALUATION"
                state["feedback"] = None
                return state

            whole_answer = (
                semantic_evidence.get("whole_answer") or {}
            )

            concept_level = (
                semantic_evidence.get("concept_level") or {}
            )

            sentence_level = (
                semantic_evidence.get("sentence_level") or {}
            )

            whole_similarity = self._safe_float(
                whole_answer.get("similarity")
            )

            concept_mean = self._safe_float(
                concept_level.get("mean_best_similarity")
            )

            sentence_mean = self._safe_float(
                sentence_level.get("mean_best_similarity")
            )

            if whole_similarity is None or concept_mean is None:
                print(
                    "Required Whole MiniLM or Concept Mean "
                    "evidence is unavailable."
                )
                state["feedback_status"] = "WAITING_FOR_EVALUATION"
                state["feedback"] = None
                return state

            feedback_evidence = (
                0.60 * concept_mean
                + 0.40 * whole_similarity
            )

            if feedback_evidence >= 0.65:

                semantic_band = "ADVANCED"

                semantic_message = (
                    "The response produced relatively strong semantic "
                    "overlap with the development reference knowledge "
                    "under the current prototype rule."
                )

            elif feedback_evidence >= 0.45:

                semantic_band = "INTERMEDIATE"

                semantic_message = (
                    "The response produced moderate semantic overlap "
                    "with the development reference knowledge under "
                    "the current prototype rule."
                )

            else:

                semantic_band = "BEGINNER"

                semantic_message = (
                    "The response produced lower semantic overlap "
                    "with the development reference knowledge under "
                    "the current prototype rule."
                )

            wpm = self._safe_float(
                features.get("wpm")
            )

            filler_count = features.get(
                "filler_count"
            )

            pause_count = features.get(
                "pause_count"
            )

            speech_observations = []

            if wpm is not None:

                speech_observations.append(
                    f"Measured speaking rate: {wpm:.1f} WPM."
                )

            if filler_count is not None:

                speech_observations.append(
                    f"Detected filler words: {filler_count}."
                )

            if pause_count is not None:

                speech_observations.append(
                    f"Detected pause intervals: {pause_count}."
                )

            feedback = {

                "type":
                    "RULE_BASED_DEVELOPMENT_PROTOTYPE",

                "whole_similarity":
                    round(whole_similarity, 4),

                "sentence_mean_similarity": (
                    round(sentence_mean, 4)
                    if sentence_mean is not None
                    else None
                ),

                "concept_mean_similarity":
                    round(concept_mean, 4),

                "feedback_evidence":
                    round(feedback_evidence, 4),

                "semantic_band":
                    semantic_band,

                "semantic_feedback":
                    semantic_message,

                "wpm":
                    wpm,

                "filler_count":
                    filler_count,

                "pause_count":
                    pause_count,

                "speech_observations":
                    speech_observations,

                "disclaimer": (
                    "Development-stage rule-based feedback only. "
                    "Not a validated competency grade, calibrated "
                    "interview score, pass/fail result, or hiring decision."
                )
            }

            state["feedback"] = feedback

            state[
                "feedback_status"
            ] = "RULE_BASED_FEEDBACK_ACTIVE"

            print(
                "Rule-based DEVELOPMENT feedback active."
            )

            print(
                "Whole MiniLM:",
                round(whole_similarity, 4)
            )

            if sentence_mean is not None:

                print(
                    "Sentence MiniLM:",
                    round(sentence_mean, 4)
                )

            print(
                "Concept Mean:",
                round(concept_mean, 4)
            )

            print(
                "Feedback evidence:",
                round(feedback_evidence, 4)
            )

            print(
                "Prototype semantic band:",
                semantic_band
            )

            print(
                "Feedback:",
                semantic_message
            )

            for observation in speech_observations:
                print(observation)

            print(
                "Development prototype only - "
                "not validated competency scoring."
            )

            return state

        # ====================================================
        # PILOT / FINAL SAFEGUARD
        # ====================================================

        scores = state.get(
            "aegie_scores"
        )

        if scores is None:

            if features:

                print(
                    "Evaluation features are available."
                )

                print(
                    "Calibrated evaluation scores are not available."
                )

                print(
                    "Final calibrated feedback generation is postponed."
                )

                state[
                    "feedback_status"
                ] = (
                    "WAITING_FOR_CALIBRATED_EVALUATION"
                )

            else:

                print(
                    "No evaluation features available."
                )

                print(
                    "Feedback generation skipped."
                )

                state[
                    "feedback_status"
                ] = "WAITING_FOR_EVALUATION"

            state["feedback"] = None

            return state

        state[
            "feedback_status"
        ] = "REPORTING_NOT_IMPLEMENTED"

        state["feedback"] = None

        print(
            "Calibrated evaluation is available, "
            "but calibrated reporting is not implemented yet."
        )

        return state


# ============================================================
# COMPLETE AEGIE PIPELINE
# ============================================================

class AEGIEAgentPipeline:

    def __init__(self):

        self.interview_agent = (
            InterviewAgent()
        )

        self.evaluation_agent = (
            EvaluationAgent()
        )

        self.adaptive_agent = (
            AdaptiveDecisionAgent()
        )

        self.feedback_agent = (
            FeedbackReportingAgent()
        )

    # ========================================================
    # RUN
    # ========================================================

    def run(
        self,
        state
    ):

        print()

        print("=" * 70)
        print("AEGIE AGENT PIPELINE")
        print("=" * 70)

        # ----------------------------------------------------
        # Interview Agent
        # ----------------------------------------------------

        state = (
            self.interview_agent.process(
                state
            )
        )

        # ----------------------------------------------------
        # Evaluation Agent
        # ----------------------------------------------------

        state = (
            self.evaluation_agent.process(
                state
            )
        )

        # ----------------------------------------------------
        # Adaptive Decision Agent
        # ----------------------------------------------------

        state = (
            self.adaptive_agent.process(
                state
            )
        )

        # ----------------------------------------------------
        # Feedback & Reporting Agent
        # ----------------------------------------------------

        state = (
            self.feedback_agent.process(
                state
            )
        )

        # ----------------------------------------------------
        # Pipeline summary
        # ----------------------------------------------------

        print()

        print("-" * 70)
        print("PIPELINE STATUS SUMMARY")
        print("-" * 70)

        print(
            "Interview Agent:",
            state.get(
                "interview_agent_status"
            )
        )

        print(
            "Evaluation Agent:",
            state.get(
                "evaluation_status"
            )
        )

        print(
            "Calibrated Scoring:",
            state.get(
                "calibrated_scoring_status"
            )
        )

        print(
            "Adaptive Agent:",
            state.get(
                "adaptive_status"
            )
        )

        print(
            "Feedback Agent:",
            state.get(
                "feedback_status"
            )
        )

        print()

        print(
            "AEGIE calibrated scores:",
            state.get(
                "aegie_scores"
            )
        )

        print(
            "Next difficulty:",
            state.get(
                "next_difficulty"
            )
        )

        print()

        print("=" * 70)
        print("PIPELINE COMPLETE")
        print("=" * 70)

        return state