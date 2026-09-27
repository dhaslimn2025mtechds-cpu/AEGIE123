# ============================================================
# AEGIE EVALUATION FEATURE BUILDER
# ============================================================
#
# Purpose:
#
# Combine three DISTINCT semantic evidence groups:
#
#   1. Whole MiniLM
#      complete candidate answer <-> complete reference_answer
#
#   2. Sentence MiniLM
#      each reference_answer sentence
#      -> best candidate-answer sentence
#
#   3. Concept Mean
#      each key_concept
#      -> best candidate-answer sentence
#
# plus objective speech measurements into one development
# research feature vector.
#
# IMPORTANT:
# - These values are FEATURES / DEVELOPMENT EVIDENCE.
# - They are NOT final AEGIE 1-5 scores.
# - No adaptive threshold is applied in this file.
# - Human annotation labels are NOT read here.
# - Development reference knowledge requires expert review
#   before final research use.
# ============================================================

import math


# ============================================================
# SAFE NUMBER CONVERSION
# ============================================================

def _safe_float(value):

    if value is None:
        return None

    try:

        number = float(value)

        if not math.isfinite(number):
            return None

        return round(
            number,
            4
        )

    except (
        TypeError,
        ValueError
    ):

        return None


def _safe_int(value):

    if value is None:
        return None

    try:

        number = int(
            value
        )

        if number < 0:
            return None

        return number

    except (
        TypeError,
        ValueError
    ):

        return None


# ============================================================
# SAFE DERIVED SPEECH FEATURES
# ============================================================

def _filler_rate_per_100_words(
    filler_count,
    word_count
):

    if (
        filler_count is None
        or word_count is None
        or word_count <= 0
    ):

        return None

    return round(
        (
            filler_count
            / word_count
        ) * 100,
        4
    )


def _pause_rate_per_minute(
    pause_count,
    duration_sec
):

    if (
        pause_count is None
        or duration_sec is None
        or duration_sec <= 0
    ):

        return None

    minutes = (
        duration_sec
        / 60.0
    )

    if minutes <= 0:
        return None

    return round(
        pause_count
        / minutes,
        4
    )


# ============================================================
# EXTRACT CORRECTED SEMANTIC FEATURES
# ============================================================

def _extract_semantic_features(
    semantic_evidence
):

    if not isinstance(
        semantic_evidence,
        dict
    ):

        return {
            "success": False,
            "reason": (
                "Semantic evidence must "
                "be a dictionary."
            ),
            "features": None
        }


    # --------------------------------------------------------
    # Correct three-part semantic structure
    # --------------------------------------------------------

    feature_summary = (
        semantic_evidence.get(
            "feature_summary"
        )
        or {}
    )


    whole_answer = (
        semantic_evidence.get(
            "whole_answer"
        )
        or {}
    )


    sentence_level = (
        semantic_evidence.get(
            "sentence_level"
        )
        or {}
    )


    concept_level = (
        semantic_evidence.get(
            "concept_level"
        )
        or {}
    )


    # --------------------------------------------------------
    # 1. WHOLE MINILM
    #
    # Exactly one whole candidate <-> whole reference cosine.
    # --------------------------------------------------------

    whole_similarity = _safe_float(

        feature_summary.get(
            "whole_similarity",
            whole_answer.get(
                "similarity"
            )
        )
    )


    # --------------------------------------------------------
    # 2. SENTENCE MINILM
    # --------------------------------------------------------

    sentence_mean = _safe_float(

        feature_summary.get(
            "sentence_mean_best_similarity",
            sentence_level.get(
                "mean_best_similarity"
            )
        )
    )


    sentence_max = _safe_float(

        feature_summary.get(
            "sentence_max_best_similarity",
            sentence_level.get(
                "max_best_similarity"
            )
        )
    )


    sentence_min = _safe_float(

        feature_summary.get(
            "sentence_min_best_similarity",
            sentence_level.get(
                "min_best_similarity"
            )
        )
    )


    # --------------------------------------------------------
    # 3. CONCEPT MEAN
    # --------------------------------------------------------

    concept_mean = _safe_float(

        feature_summary.get(
            "concept_mean_best_similarity",
            concept_level.get(
                "mean_best_similarity"
            )
        )
    )


    concept_max = _safe_float(

        feature_summary.get(
            "concept_max_best_similarity",
            concept_level.get(
                "max_best_similarity"
            )
        )
    )


    concept_min = _safe_float(

        feature_summary.get(
            "concept_min_best_similarity",
            concept_level.get(
                "min_best_similarity"
            )
        )
    )


    # --------------------------------------------------------
    # Semantic structure counts
    # --------------------------------------------------------

    reference_sentence_count = _safe_int(

        feature_summary.get(
            "reference_sentence_count",
            sentence_level.get(
                "reference_sentence_count"
            )
        )
    )


    answer_sentence_count = _safe_int(

        feature_summary.get(
            "answer_sentence_count",
            sentence_level.get(
                "candidate_sentence_count"
            )
        )
    )


    reference_concept_count = _safe_int(

        feature_summary.get(
            "reference_concept_count",
            concept_level.get(
                "concept_count",
                semantic_evidence.get(
                    "reference_concept_count"
                )
            )
        )
    )


    # --------------------------------------------------------
    # Require all three main semantic measurements.
    #
    # This prevents accidental fallback to the old duplicated
    # semantic architecture.
    # --------------------------------------------------------

    required_main_values = {

        "whole_similarity":
            whole_similarity,

        "sentence_mean_best_similarity":
            sentence_mean,

        "concept_mean_best_similarity":
            concept_mean
    }


    missing = [

        name

        for name, value
        in required_main_values.items()

        if value is None
    ]


    if missing:

        return {
            "success": False,
            "reason": (
                "Corrected three-part semantic evidence "
                "is incomplete. Missing: "
                + ", ".join(
                    missing
                )
            ),
            "features": None
        }


    return {

        "success": True,

        "reason": None,

        "features": {

            # WHOLE MINILM
            "whole_similarity":
                whole_similarity,

            # SENTENCE MINILM
            "sentence_mean_best_similarity":
                sentence_mean,

            "sentence_max_best_similarity":
                sentence_max,

            "sentence_min_best_similarity":
                sentence_min,

            # CONCEPT MEAN
            "concept_mean_best_similarity":
                concept_mean,

            "concept_max_best_similarity":
                concept_max,

            "concept_min_best_similarity":
                concept_min,

            # STRUCTURE COUNTS
            "reference_sentence_count":
                reference_sentence_count,

            "answer_sentence_count":
                answer_sentence_count,

            "reference_concept_count":
                reference_concept_count
        }
    }


# ============================================================
# BUILD EVALUATION FEATURE VECTOR
# ============================================================

def build_evaluation_features(
    state
):

    # --------------------------------------------------------
    # Validate state
    # --------------------------------------------------------

    if not isinstance(
        state,
        dict
    ):

        return {
            "success": False,
            "status": "INVALID_STATE",
            "reason": (
                "State must be a dictionary."
            ),
            "features": None
        }


    # --------------------------------------------------------
    # Semantic evidence
    # --------------------------------------------------------

    semantic_evidence = state.get(
        "semantic_evidence"
    )


    if not isinstance(
        semantic_evidence,
        dict
    ):

        return {
            "success": False,
            "status":
                "SEMANTIC_EVIDENCE_MISSING",
            "reason": (
                "Semantic evidence "
                "is not available."
            ),
            "features": None
        }


    semantic_result = (
        _extract_semantic_features(
            semantic_evidence
        )
    )


    if not semantic_result[
        "success"
    ]:

        return {
            "success": False,
            "status":
                "SEMANTIC_EVIDENCE_NOT_READY",
            "reason":
                semantic_result[
                    "reason"
                ],
            "features": None
        }


    semantic_features = (
        semantic_result[
            "features"
        ]
    )


    # --------------------------------------------------------
    # Current question
    # --------------------------------------------------------

    current_question = (
        state.get(
            "current_question"
        )
        or {}
    )


    # --------------------------------------------------------
    # Objective speech features
    # --------------------------------------------------------

    duration_sec = _safe_float(
        state.get(
            "duration_sec"
        )
    )


    word_count = _safe_int(
        state.get(
            "word_count"
        )
    )


    wpm = _safe_float(
        state.get(
            "wpm"
        )
    )


    filler_count = _safe_int(
        state.get(
            "filler_count"
        )
    )


    pause_count = _safe_int(
        state.get(
            "pause_count"
        )
    )


    # --------------------------------------------------------
    # Derived objective speech features
    # --------------------------------------------------------

    filler_rate = (
        _filler_rate_per_100_words(
            filler_count,
            word_count
        )
    )


    pause_rate = (
        _pause_rate_per_minute(
            pause_count,
            duration_sec
        )
    )


    # --------------------------------------------------------
    # Construct corrected feature vector
    # --------------------------------------------------------

    features = {

        # ====================================================
        # DEVELOPMENT / RESEARCH METADATA
        # ====================================================

        "participant_id":
            state.get(
                "participant_id"
            ),

        "job_role":
            state.get(
                "job_role"
            ),

        "question_id":
            current_question.get(
                "question_id"
            ),

        "difficulty":
            current_question.get(
                "difficulty"
            ),


        # ====================================================
        # 1. WHOLE MINILM
        # ====================================================

        "whole_similarity":
            semantic_features[
                "whole_similarity"
            ],


        # ====================================================
        # 2. SENTENCE MINILM
        # ====================================================

        "sentence_mean_best_similarity":
            semantic_features[
                "sentence_mean_best_similarity"
            ],

        "sentence_max_best_similarity":
            semantic_features[
                "sentence_max_best_similarity"
            ],

        "sentence_min_best_similarity":
            semantic_features[
                "sentence_min_best_similarity"
            ],


        # ====================================================
        # 3. CONCEPT MEAN
        # ====================================================

        "concept_mean_best_similarity":
            semantic_features[
                "concept_mean_best_similarity"
            ],

        "concept_max_best_similarity":
            semantic_features[
                "concept_max_best_similarity"
            ],

        "concept_min_best_similarity":
            semantic_features[
                "concept_min_best_similarity"
            ],


        # ====================================================
        # SEMANTIC STRUCTURE
        # ====================================================

        "reference_sentence_count":
            semantic_features[
                "reference_sentence_count"
            ],

        "answer_sentence_count":
            semantic_features[
                "answer_sentence_count"
            ],

        "reference_concept_count":
            semantic_features[
                "reference_concept_count"
            ],


        # ====================================================
        # OBJECTIVE SPEECH FEATURES
        # ====================================================

        "duration_sec":
            duration_sec,

        "word_count":
            word_count,

        "wpm":
            wpm,

        "filler_count":
            filler_count,

        "pause_count":
            pause_count,


        # ====================================================
        # DERIVED OBJECTIVE SPEECH FEATURES
        # ====================================================

        "filler_rate_per_100_words":
            filler_rate,

        "pause_rate_per_minute":
            pause_rate
    }


    # --------------------------------------------------------
    # Return
    # --------------------------------------------------------

    return {

        "success": True,

        "status":
            "EVALUATION_FEATURES_READY",

        "reason":
            None,

        "features":
            features
    }


# ============================================================
# DEVELOPMENT TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("AEGIE CORRECTED EVALUATION FEATURE BUILDER TEST")
    print("=" * 70)


    # --------------------------------------------------------
    # Development-only state.
    #
    # Mirrors the corrected semantic_evaluator.py structure.
    # This is NOT participant research data.
    # --------------------------------------------------------

    development_state = {

        "participant_id":
            "DEV_TEST",

        "job_role":
            "Cybersecurity Analyst",

        "current_question": {

            "question_id":
                "CS_E02",

            "difficulty":
                "Easy",

            "question_text":
                (
                    "What is the difference between "
                    "authentication and authorization?"
                )
        },


        # ----------------------------------------------------
        # Objective speech features
        # ----------------------------------------------------

        "duration_sec":
            20.0,

        "word_count":
            43,

        "wpm":
            129.0,

        "filler_count":
            1,

        "pause_count":
            2,


        # ----------------------------------------------------
        # Correct THREE-PART semantic evidence structure
        # ----------------------------------------------------

        "semantic_evidence": {

            "question_id":
                "CS_E02",

            "reference_role":
                "Cybersecurity Analyst",

            "reference_concept_count":
                4,


            "whole_answer": {

                "status":
                    "WHOLE_ANSWER_EVIDENCE_READY",

                "similarity":
                    0.8699,

                "comparison":
                    (
                        "complete candidate transcript "
                        "<-> complete reference_answer"
                    )
            },


            "sentence_level": {

                "status":
                    "SENTENCE_ANSWER_EVIDENCE_READY",

                "reference_sentence_count":
                    3,

                "candidate_sentence_count":
                    4,

                "mean_best_similarity":
                    0.7681,

                "max_best_similarity":
                    0.7998,

                "min_best_similarity":
                    0.7126,

                "sentence_results":
                    []
            },


            "concept_level": {

                "status":
                    "SENTENCE_CONCEPT_EVIDENCE_READY",

                "sentence_count":
                    4,

                "concept_count":
                    4,

                "mean_best_similarity":
                    0.8373,

                "max_best_similarity":
                    0.9262,

                "min_best_similarity":
                    0.7126,

                "concept_results":
                    []
            },


            "feature_summary": {

                "whole_similarity":
                    0.8699,

                "sentence_mean_best_similarity":
                    0.7681,

                "sentence_max_best_similarity":
                    0.7998,

                "sentence_min_best_similarity":
                    0.7126,

                "concept_mean_best_similarity":
                    0.8373,

                "concept_max_best_similarity":
                    0.9262,

                "concept_min_best_similarity":
                    0.7126,

                "reference_sentence_count":
                    3,

                "answer_sentence_count":
                    4,

                "reference_concept_count":
                    4
            }
        }
    }


    # --------------------------------------------------------
    # Build feature vector
    # --------------------------------------------------------

    result = (
        build_evaluation_features(
            development_state
        )
    )


    print()

    print(
        "Success:",
        result[
            "success"
        ]
    )

    print(
        "Status:",
        result[
            "status"
        ]
    )

    print(
        "Reason:",
        result[
            "reason"
        ]
    )


    if result[
        "success"
    ]:

        features = result[
            "features"
        ]


        print()
        print("-" * 70)
        print("THREE DISTINCT SEMANTIC FEATURES")
        print("-" * 70)

        print(
            "Whole MiniLM:",
            features[
                "whole_similarity"
            ]
        )

        print(
            "Sentence MiniLM Mean:",
            features[
                "sentence_mean_best_similarity"
            ]
        )

        print(
            "Concept Mean:",
            features[
                "concept_mean_best_similarity"
            ]
        )


        print()
        print("-" * 70)
        print("COMPLETE DEVELOPMENT FEATURE VECTOR")
        print("-" * 70)


        for key, value in (
            features.items()
        ):

            print(
                f"{key}: {value}"
            )


        print()
        print("=" * 70)

        print(
            "PASS: CORRECTED THREE-PART "
            "FEATURE VECTOR GENERATED"
        )

        print("=" * 70)

    else:

        print()
        print("=" * 70)

        print(
            "FAIL: CORRECTED FEATURE "
            "VECTOR WAS NOT GENERATED"
        )

        print("=" * 70)


    print()
    print("Whole MiniLM included: YES")
    print("Sentence MiniLM included: YES")
    print("Concept Mean included: YES")
    print("Objective speech features included: YES")
    print("Derived speech features included: YES")
    print("Human annotation labels used: NO")
    print("Final AEGIE 1-5 scores generated: NO")
    print("Adaptive threshold applied here: NO")

    print(
        "Development reference knowledge only; "
        "expert review is required before final research use."
    )