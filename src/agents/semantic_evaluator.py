# ============================================================
# AEGIE SEMANTIC EVALUATION AGENT
# ============================================================
#
# Purpose:
# Prepare three DISTINCT MiniLM semantic evidence measurements
# for the AEGIE Evaluation Agent.
#
# Current development pipeline:
#
# Question + Transcript
#        |
#        v
# Central 72-Question Reference Registry
#        |
#        +--> Whole MiniLM
#        |    complete candidate answer
#        |    <-> complete reference_answer
#        |
#        +--> Sentence MiniLM
#        |    each reference_answer sentence
#        |    -> best candidate-answer sentence
#        |
#        +--> Concept Mean
#             each key_concept
#             -> best candidate-answer sentence
#        |
#        v
# Semantic Evidence
#
# IMPORTANT:
# - Human annotation labels are NEVER read here.
# - Semantic similarity is NOT a final 1-5 score.
# - No pass/fail threshold is applied here.
# - No adaptive threshold is applied by this evaluator.
# - Development reference knowledge requires expert review
#   before final research use.
# ============================================================


# ============================================================
# PACKAGE-SAFE IMPORTS
# ============================================================

try:

    from .reference_registry import (
        get_reference_answer
    )

    from .evaluation_schema import (
        create_evaluation_input,
        validate_aegie_scores
    )

    from .evaluation_rubric import (
        get_evaluation_rubric
    )

    from .whole_answer_evaluator import (
        WholeAnswerEvaluator
    )

    from .sentence_answer_evaluator import (
        SentenceAnswerEvaluator
    )

    from .sentence_concept_evaluator import (
        SentenceConceptEvaluator
    )

except ImportError:

    from reference_registry import (
        get_reference_answer
    )

    from evaluation_schema import (
        create_evaluation_input,
        validate_aegie_scores
    )

    from evaluation_rubric import (
        get_evaluation_rubric
    )

    from whole_answer_evaluator import (
        WholeAnswerEvaluator
    )

    from sentence_answer_evaluator import (
        SentenceAnswerEvaluator
    )

    from sentence_concept_evaluator import (
        SentenceConceptEvaluator
    )


# ============================================================
# LAZY EVALUATOR CACHE
# ============================================================
#
# All three evaluators use get_shared_minilm_embedder().
# Therefore MiniLM is loaded once and reused.
# ============================================================

_WHOLE_ANSWER_EVALUATOR = None
_SENTENCE_ANSWER_EVALUATOR = None
_SENTENCE_CONCEPT_EVALUATOR = None


def get_whole_answer_evaluator():

    global _WHOLE_ANSWER_EVALUATOR

    if _WHOLE_ANSWER_EVALUATOR is None:

        _WHOLE_ANSWER_EVALUATOR = (
            WholeAnswerEvaluator()
        )

    return _WHOLE_ANSWER_EVALUATOR


def get_sentence_answer_evaluator():

    global _SENTENCE_ANSWER_EVALUATOR

    if _SENTENCE_ANSWER_EVALUATOR is None:

        _SENTENCE_ANSWER_EVALUATOR = (
            SentenceAnswerEvaluator()
        )

    return _SENTENCE_ANSWER_EVALUATOR


def get_sentence_concept_evaluator():

    global _SENTENCE_CONCEPT_EVALUATOR

    if _SENTENCE_CONCEPT_EVALUATOR is None:

        _SENTENCE_CONCEPT_EVALUATOR = (
            SentenceConceptEvaluator()
        )

    return _SENTENCE_CONCEPT_EVALUATOR


# ============================================================
# EMPTY FAILURE RESPONSE
# ============================================================

def build_failure_response(
    status,
    reason
):

    return {
        "ready": False,
        "status": status,
        "reason": reason,
        "evaluation_context": None,
        "semantic_evidence": None,
        "scores": None
    }


# ============================================================
# PREPARE SEMANTIC EVALUATION
# ============================================================

def prepare_semantic_evaluation(
    state,
    generate_semantic_evidence=True
):

    # --------------------------------------------------------
    # 1. Validate basic evaluation input
    # --------------------------------------------------------

    input_result = (
        create_evaluation_input(
            state
        )
    )

    if not input_result["ready"]:

        return build_failure_response(
            status="WAITING_FOR_INPUT",
            reason=input_result["reason"]
        )

    evaluation_data = input_result[
        "data"
    ]

    # --------------------------------------------------------
    # 2. Question ID
    # --------------------------------------------------------

    question_id = evaluation_data[
        "question_id"
    ]

    if question_id is None:

        return build_failure_response(
            status="QUESTION_ID_MISSING",
            reason="Question ID is unavailable."
        )

    question_id = str(
        question_id
    ).strip()

    if not question_id:

        return build_failure_response(
            status="QUESTION_ID_EMPTY",
            reason="Question ID is empty."
        )

    # --------------------------------------------------------
    # 3. Retrieve reference from CENTRAL REGISTRY
    # --------------------------------------------------------

    reference = get_reference_answer(
        question_id
    )

    if reference is None:

        return build_failure_response(
            status="REFERENCE_NOT_FOUND",
            reason=(
                f"No semantic reference "
                f"found for {question_id}."
            )
        )

    reference_answer = reference.get(
        "reference_answer"
    )

    if reference_answer is None:

        return build_failure_response(
            status="REFERENCE_ANSWER_MISSING",
            reason=(
                f"No reference_answer found "
                f"for {question_id}."
            )
        )

    reference_answer = str(
        reference_answer
    ).strip()

    if not reference_answer:

        return build_failure_response(
            status="REFERENCE_ANSWER_EMPTY",
            reason=(
                f"reference_answer is empty "
                f"for {question_id}."
            )
        )

    # --------------------------------------------------------
    # 4. Evaluation rubric
    # --------------------------------------------------------

    rubric = (
        get_evaluation_rubric()
    )

    # --------------------------------------------------------
    # 5. Speech features
    # --------------------------------------------------------

    speech_features = {

        "duration_sec":
            evaluation_data.get(
                "duration_sec"
            ),

        "word_count":
            evaluation_data.get(
                "word_count"
            ),

        "wpm":
            evaluation_data.get(
                "wpm"
            ),

        "filler_count":
            evaluation_data.get(
                "filler_count"
            ),

        "pause_count":
            evaluation_data.get(
                "pause_count"
            )
    }

    # --------------------------------------------------------
    # 6. Build evaluation context
    # --------------------------------------------------------

    context = {

        "question_id":
            question_id,

        "job_role":
            reference.get(
                "job_role"
            ),

        "question_text":
            evaluation_data[
                "question_text"
            ],

        "difficulty":
            evaluation_data[
                "difficulty"
            ],

        "participant_transcript":
            evaluation_data[
                "transcript"
            ],

        "reference_question":
            reference.get(
                "question"
            ),

        "reference_answer":
            reference_answer,

        "reference_key_concepts":
            reference.get(
                "key_concepts",
                []
            ),

        "acceptable_examples":
            reference.get(
                "acceptable_examples",
                []
            ),

        "speech_features":
            speech_features,

        "rubric":
            rubric
    }

    # --------------------------------------------------------
    # 7. Context-only mode
    # --------------------------------------------------------

    if not generate_semantic_evidence:

        return {

            "ready": True,

            "status":
                "READY_FOR_SEMANTIC_MODEL",

            "reason":
                None,

            "evaluation_context":
                context,

            "semantic_evidence":
                None,

            "scores":
                None
        }

    # --------------------------------------------------------
    # 8. TRUE WHOLE-ANSWER MINILM
    #
    # Complete candidate transcript
    # <-> complete reference_answer
    # --------------------------------------------------------

    try:

        whole_evaluator = (
            get_whole_answer_evaluator()
        )

        whole_answer_result = (
            whole_evaluator.evaluate(
                question_id=
                    question_id,

                transcript=
                    evaluation_data[
                        "transcript"
                    ]
            )
        )

    except Exception as error:

        return build_failure_response(
            status=(
                "WHOLE_ANSWER_EVALUATION_ERROR"
            ),
            reason=str(error)
        )

    if not whole_answer_result.get(
        "success"
    ):

        return build_failure_response(
            status=whole_answer_result.get(
                "status",
                "WHOLE_ANSWER_EVALUATION_FAILED"
            ),
            reason=whole_answer_result.get(
                "reason",
                "Whole-answer semantic evaluation failed."
            )
        )

    # --------------------------------------------------------
    # 9. TRUE SENTENCE MINILM
    #
    # Each reference_answer sentence
    # -> best candidate-answer sentence
    # --------------------------------------------------------

    try:

        sentence_evaluator = (
            get_sentence_answer_evaluator()
        )

        sentence_result = (
            sentence_evaluator.evaluate(
                question_id=
                    question_id,

                transcript=
                    evaluation_data[
                        "transcript"
                    ]
            )
        )

    except Exception as error:

        return build_failure_response(
            status=(
                "SENTENCE_ANSWER_EVALUATION_ERROR"
            ),
            reason=str(error)
        )

    if not sentence_result.get(
        "success"
    ):

        return build_failure_response(
            status=sentence_result.get(
                "status",
                "SENTENCE_ANSWER_EVALUATION_FAILED"
            ),
            reason=sentence_result.get(
                "reason",
                "Sentence-answer semantic evaluation failed."
            )
        )

    # --------------------------------------------------------
    # 10. CONCEPT MEAN
    #
    # Each key_concept
    # -> best candidate-answer sentence
    # --------------------------------------------------------

    try:

        concept_evaluator = (
            get_sentence_concept_evaluator()
        )

        concept_result = (
            concept_evaluator.evaluate(
                question_id=
                    question_id,

                transcript=
                    evaluation_data[
                        "transcript"
                    ]
            )
        )

    except Exception as error:

        return build_failure_response(
            status=(
                "CONCEPT_EVALUATION_ERROR"
            ),
            reason=str(error)
        )

    if not concept_result.get(
        "success"
    ):

        return build_failure_response(
            status=concept_result.get(
                "status",
                "CONCEPT_EVALUATION_FAILED"
            ),
            reason=(
                "Concept-level semantic "
                "evaluation failed."
            )
        )

    # --------------------------------------------------------
    # 11. Combine THREE DISTINCT semantic evidence groups
    # --------------------------------------------------------

    whole_similarity = (
        whole_answer_result.get(
            "similarity"
        )
    )

    sentence_mean = (
        sentence_result.get(
            "mean_best_similarity"
        )
    )

    concept_mean = (
        concept_result.get(
            "mean_best_similarity"
        )
    )

    semantic_evidence = {

        "question_id":
            question_id,

        "reference_role":
            reference.get(
                "job_role"
            ),

        "reference_concept_count":
            len(
                reference.get(
                    "key_concepts",
                    []
                )
            ),

        # ====================================================
        # A. WHOLE MINILM
        # ====================================================

        "whole_answer": {

            "status":
                whole_answer_result.get(
                    "status"
                ),

            "similarity":
                whole_similarity,

            "comparison":
                (
                    "complete candidate transcript "
                    "<-> complete reference_answer"
                )
        },

        # ====================================================
        # B. SENTENCE MINILM
        # ====================================================

        "sentence_level": {

            "status":
                sentence_result.get(
                    "status"
                ),

            "reference_sentence_count":
                sentence_result.get(
                    "reference_sentence_count"
                ),

            "candidate_sentence_count":
                sentence_result.get(
                    "candidate_sentence_count"
                ),

            "mean_best_similarity":
                sentence_mean,

            "max_best_similarity":
                sentence_result.get(
                    "max_best_similarity"
                ),

            "min_best_similarity":
                sentence_result.get(
                    "min_best_similarity"
                ),

            "sentence_results":
                sentence_result.get(
                    "sentence_results",
                    []
                )
        },

        # ====================================================
        # C. CONCEPT MEAN
        # ====================================================

        "concept_level": {

            "status":
                concept_result.get(
                    "status"
                ),

            "sentence_count":
                concept_result.get(
                    "sentence_count"
                ),

            "concept_count":
                concept_result.get(
                    "concept_count"
                ),

            "mean_best_similarity":
                concept_mean,

            "max_best_similarity":
                concept_result.get(
                    "max_best_similarity"
                ),

            "min_best_similarity":
                concept_result.get(
                    "min_best_similarity"
                ),

            "concept_results":
                concept_result.get(
                    "concept_results",
                    []
                )
        }
    }

    # --------------------------------------------------------
    # 12. Semantic feature summary
    #
    # Threshold-free numeric evidence only.
    # --------------------------------------------------------

    semantic_feature_summary = {

        "whole_similarity":
            whole_similarity,

        "sentence_mean_best_similarity":
            sentence_mean,

        "sentence_max_best_similarity":
            sentence_result.get(
                "max_best_similarity"
            ),

        "sentence_min_best_similarity":
            sentence_result.get(
                "min_best_similarity"
            ),

        "concept_mean_best_similarity":
            concept_mean,

        "concept_max_best_similarity":
            concept_result.get(
                "max_best_similarity"
            ),

        "concept_min_best_similarity":
            concept_result.get(
                "min_best_similarity"
            ),

        "reference_sentence_count":
            sentence_result.get(
                "reference_sentence_count"
            ),

        "answer_sentence_count":
            sentence_result.get(
                "candidate_sentence_count"
            ),

        "reference_concept_count":
            concept_result.get(
                "concept_count"
            )
    }

    semantic_evidence[
        "feature_summary"
    ] = semantic_feature_summary

    # --------------------------------------------------------
    # 13. Successful result
    # --------------------------------------------------------

    return {

        "ready": True,

        "status":
            "SEMANTIC_EVIDENCE_READY",

        "reason":
            None,

        "evaluation_context":
            context,

        "semantic_evidence":
            semantic_evidence,

        # No calibrated 1-5 scoring model is produced here.
        "scores":
            None
    }


# ============================================================
# STORE MODEL OUTPUT SAFELY
# ============================================================

def accept_model_scores(scores):

    validation = (
        validate_aegie_scores(
            scores
        )
    )

    if not validation[
        "valid"
    ]:

        return {
            "accepted": False,
            "reason": validation[
                "reason"
            ],
            "scores": None
        }

    return {
        "accepted": True,
        "reason": None,
        "scores": scores
    }


# ============================================================
# DEVELOPMENT TEST
# ============================================================

def main():

    print("=" * 70)
    print("AEGIE THREE-PART SEMANTIC EVALUATION TEST")
    print("=" * 70)

    # ========================================================
    # TEST 1
    # Missing transcript.
    # ========================================================

    state_without_transcript = {

        "participant_id":
            "DEV_TEST",

        "job_role":
            "Cybersecurity Analyst",

        "current_question": {

            "question_id":
                "CS_E02",

            "question_text":
                (
                    "What is the difference between "
                    "authentication and authorization?"
                ),

            "difficulty":
                "Easy"
        },

        "transcript":
            None,

        "duration_sec":
            15.0,

        "word_count":
            None,

        "wpm":
            None,

        "filler_count":
            None,

        "pause_count":
            1
    }

    result = (
        prepare_semantic_evaluation(
            state_without_transcript
        )
    )

    print()
    print("-" * 70)
    print("TEST 1 - NO TRANSCRIPT")
    print("-" * 70)

    print(
        "Ready:",
        result[
            "ready"
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

    # ========================================================
    # TEST 2
    # Development-only transcript.
    # ========================================================

    state_with_test_transcript = {

        "participant_id":
            "DEV_TEST",

        "job_role":
            "Cybersecurity Analyst",

        "current_question": {

            "question_id":
                "CS_E02",

            "question_text":
                (
                    "What is the difference between "
                    "authentication and authorization?"
                ),

            "difficulty":
                "Easy"
        },

        "transcript": (

            "Authentication verifies the identity "
            "of a user. "

            "A password or another authentication "
            "factor can help verify who the user is. "

            "Authorization determines what an "
            "authenticated user is permitted to "
            "access or perform. "

            "For example, an administrator can have "
            "permissions that a normal user does not."
        ),

        "duration_sec":
            20.0,

        "word_count":
            43,

        "wpm":
            129.0,

        "filler_count":
            0,

        "pause_count":
            2
    }

    result = (
        prepare_semantic_evaluation(
            state_with_test_transcript
        )
    )

    print()
    print("-" * 70)
    print("TEST 2 - THREE DISTINCT SEMANTIC MEASUREMENTS")
    print("-" * 70)

    print(
        "Ready:",
        result[
            "ready"
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

    if not result[
        "ready"
    ]:

        print()

        print(
            "FAIL: Semantic evaluation "
            "did not complete."
        )

        return

    evidence = result[
        "semantic_evidence"
    ]

    whole = evidence[
        "whole_answer"
    ]

    sentence = evidence[
        "sentence_level"
    ]

    concept = evidence[
        "concept_level"
    ]

    print()
    print("-" * 70)
    print("1. WHOLE MINILM")
    print("-" * 70)

    print(
        "Whole similarity:",
        whole[
            "similarity"
        ]
    )

    print(
        "Method:",
        whole[
            "comparison"
        ]
    )

    print()
    print("-" * 70)
    print("2. SENTENCE MINILM")
    print("-" * 70)

    print(
        "Reference sentences:",
        sentence[
            "reference_sentence_count"
        ]
    )

    print(
        "Candidate sentences:",
        sentence[
            "candidate_sentence_count"
        ]
    )

    print(
        "Mean best similarity:",
        sentence[
            "mean_best_similarity"
        ]
    )

    print(
        "Maximum best similarity:",
        sentence[
            "max_best_similarity"
        ]
    )

    print(
        "Minimum best similarity:",
        sentence[
            "min_best_similarity"
        ]
    )

    print()
    print("-" * 70)
    print("3. CONCEPT MEAN")
    print("-" * 70)

    print(
        "Reference concepts:",
        concept[
            "concept_count"
        ]
    )

    print(
        "Candidate sentences:",
        concept[
            "sentence_count"
        ]
    )

    print(
        "Mean best similarity:",
        concept[
            "mean_best_similarity"
        ]
    )

    print(
        "Maximum best similarity:",
        concept[
            "max_best_similarity"
        ]
    )

    print(
        "Minimum best similarity:",
        concept[
            "min_best_similarity"
        ]
    )

    print()
    print("-" * 70)
    print("THREE-PART FEATURE SUMMARY")
    print("-" * 70)

    for key, value in evidence[
        "feature_summary"
    ].items():

        print(
            f"{key}: {value}"
        )

    print()
    print("AEGIE 1-5 scores:", result["scores"])

    print()
    print("=" * 70)

    print(
        "PASS: THREE DISTINCT SEMANTIC "
        "MEASUREMENTS GENERATED"
    )

    print("=" * 70)

    print()
    print("Whole MiniLM: PASS")
    print("Sentence MiniLM: PASS")
    print("Concept Mean: PASS")
    print("Central 72-question registry: PASS")
    print("Human labels used: NO")
    print("Similarity threshold used here: NO")
    print("Final AEGIE 1-5 scores generated: NO")

    print(
        "Development reference knowledge only; "
        "expert review is required before final research use."
    )


# ============================================================
# RUN DEVELOPMENT TEST
# ============================================================

if __name__ == "__main__":

    main()