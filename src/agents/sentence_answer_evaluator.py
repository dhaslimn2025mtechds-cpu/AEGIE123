# ============================================================
# AEGIE TRUE SENTENCE-LEVEL SEMANTIC EVALUATOR
# ============================================================
#
# Development semantic evidence component.
#
# Purpose:
# Compare sentences from the complete development
# reference_answer with sentences from the candidate transcript.
#
# Method:
# 1. Split reference_answer into sentences.
# 2. Split candidate transcript into sentences.
# 3. Compare every reference sentence with every candidate sentence.
# 4. Keep the best candidate-sentence match for each
#    reference sentence.
# 5. Report mean, maximum and minimum best similarity.
#
# IMPORTANT:
# - This is different from concept-level evidence.
# - key_concepts are NOT used by this evaluator.
# - Similarities are semantic evidence/features only.
# - They are NOT final 1-5 AEGIE scores.
# - No pass/fail or adaptive threshold is applied here.
# - Development reference knowledge requires expert review
#   before final research use.
# ============================================================


import re
import numpy as np


# ============================================================
# PACKAGE-SAFE IMPORTS
# ============================================================

try:

    from .minilm_embedder import (
        get_shared_minilm_embedder,
        cosine_similarity
    )

    from .reference_registry import (
        get_reference_answer
    )

except ImportError:

    from minilm_embedder import (
        get_shared_minilm_embedder,
        cosine_similarity
    )

    from reference_registry import (
        get_reference_answer
    )


# ============================================================
# SENTENCE ANSWER EVALUATOR
# ============================================================

class SentenceAnswerEvaluator:

    def __init__(self):

        self.embedder = get_shared_minilm_embedder()


    # --------------------------------------------------------
    # Sentence splitting
    # --------------------------------------------------------

    @staticmethod
    def split_sentences(text):

        if not text:
            return []

        text = str(text).strip()

        if not text:
            return []

        sentences = re.split(
            r'(?<=[.!?])\s+',
            text
        )

        return [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]


    # --------------------------------------------------------
    # Evaluation
    # --------------------------------------------------------

    def evaluate(
        self,
        question_id,
        transcript
    ):

        # ----------------------------------------------------
        # Validate question ID
        # ----------------------------------------------------

        if question_id is None:

            return {
                "success": False,
                "status": "QUESTION_ID_MISSING",
                "question_id": None,
                "sentence_results": [],
                "mean_best_similarity": None,
                "max_best_similarity": None,
                "min_best_similarity": None,
                "reason": "Question ID is unavailable."
            }


        question_id = str(
            question_id
        ).strip()


        if not question_id:

            return {
                "success": False,
                "status": "QUESTION_ID_EMPTY",
                "question_id": question_id,
                "sentence_results": [],
                "mean_best_similarity": None,
                "max_best_similarity": None,
                "min_best_similarity": None,
                "reason": "Question ID is empty."
            }


        # ----------------------------------------------------
        # Validate candidate transcript
        # ----------------------------------------------------

        if transcript is None:

            return {
                "success": False,
                "status": "TRANSCRIPT_MISSING",
                "question_id": question_id,
                "sentence_results": [],
                "mean_best_similarity": None,
                "max_best_similarity": None,
                "min_best_similarity": None,
                "reason": "Transcript is unavailable."
            }


        transcript = str(
            transcript
        ).strip()


        if not transcript:

            return {
                "success": False,
                "status": "TRANSCRIPT_EMPTY",
                "question_id": question_id,
                "sentence_results": [],
                "mean_best_similarity": None,
                "max_best_similarity": None,
                "min_best_similarity": None,
                "reason": "Transcript is empty."
            }


        # ----------------------------------------------------
        # Retrieve central reference
        # ----------------------------------------------------

        reference = get_reference_answer(
            question_id
        )


        if reference is None:

            return {
                "success": False,
                "status": "REFERENCE_NOT_FOUND",
                "question_id": question_id,
                "sentence_results": [],
                "mean_best_similarity": None,
                "max_best_similarity": None,
                "min_best_similarity": None,
                "reason": (
                    f"No reference knowledge found "
                    f"for {question_id}."
                )
            }


        reference_role = reference.get(
            "job_role"
        )


        reference_question = reference.get(
            "question"
        )


        reference_answer = reference.get(
            "reference_answer"
        )


        if reference_answer is None:

            return {
                "success": False,
                "status": "REFERENCE_ANSWER_MISSING",
                "question_id": question_id,
                "reference_role": reference_role,
                "sentence_results": [],
                "mean_best_similarity": None,
                "max_best_similarity": None,
                "min_best_similarity": None,
                "reason": (
                    "Development reference_answer "
                    "is unavailable."
                )
            }


        reference_answer = str(
            reference_answer
        ).strip()


        if not reference_answer:

            return {
                "success": False,
                "status": "REFERENCE_ANSWER_EMPTY",
                "question_id": question_id,
                "reference_role": reference_role,
                "sentence_results": [],
                "mean_best_similarity": None,
                "max_best_similarity": None,
                "min_best_similarity": None,
                "reason": (
                    "Development reference_answer is empty."
                )
            }


        # ----------------------------------------------------
        # Split candidate and reference answers
        # ----------------------------------------------------

        candidate_sentences = self.split_sentences(
            transcript
        )


        reference_sentences = self.split_sentences(
            reference_answer
        )


        if not candidate_sentences:

            return {
                "success": False,
                "status": "NO_CANDIDATE_SENTENCES",
                "question_id": question_id,
                "sentence_results": [],
                "mean_best_similarity": None,
                "max_best_similarity": None,
                "min_best_similarity": None,
                "reason": (
                    "No candidate-answer sentences "
                    "were available."
                )
            }


        if not reference_sentences:

            return {
                "success": False,
                "status": "NO_REFERENCE_SENTENCES",
                "question_id": question_id,
                "sentence_results": [],
                "mean_best_similarity": None,
                "max_best_similarity": None,
                "min_best_similarity": None,
                "reason": (
                    "No reference-answer sentences "
                    "were available."
                )
            }


        # ----------------------------------------------------
        # Encode all sentences in one MiniLM batch
        # ----------------------------------------------------

        all_texts = (
            candidate_sentences
            + reference_sentences
        )


        embeddings = self.embedder.encode(
            all_texts
        )


        candidate_count = len(
            candidate_sentences
        )


        candidate_embeddings = (
            embeddings[
                :candidate_count
            ]
        )


        reference_embeddings = (
            embeddings[
                candidate_count:
            ]
        )


        # ----------------------------------------------------
        # Reference sentence -> best candidate sentence
        # ----------------------------------------------------

        sentence_results = []


        for reference_index, (
            reference_sentence,
            reference_embedding
        ) in enumerate(

            zip(
                reference_sentences,
                reference_embeddings
            ),

            start=1
        ):

            similarities = []


            for candidate_index, (
                candidate_sentence,
                candidate_embedding
            ) in enumerate(

                zip(
                    candidate_sentences,
                    candidate_embeddings
                ),

                start=1
            ):

                score = cosine_similarity(
                    reference_embedding,
                    candidate_embedding
                )


                similarities.append(
                    {
                        "candidate_sentence_number":
                            candidate_index,

                        "candidate_sentence":
                            candidate_sentence,

                        "similarity":
                            round(
                                float(score),
                                4
                            )
                    }
                )


            best_match = max(
                similarities,
                key=lambda item:
                    item["similarity"]
            )


            sentence_results.append(
                {
                    "reference_sentence_number":
                        reference_index,

                    "reference_sentence":
                        reference_sentence,

                    "best_similarity":
                        best_match[
                            "similarity"
                        ],

                    "best_candidate_sentence_number":
                        best_match[
                            "candidate_sentence_number"
                        ],

                    "best_candidate_sentence":
                        best_match[
                            "candidate_sentence"
                        ]
                }
            )


        # ----------------------------------------------------
        # Aggregate true sentence-level evidence
        # ----------------------------------------------------

        best_scores = [

            item[
                "best_similarity"
            ]

            for item in sentence_results
        ]


        mean_best_similarity = float(
            np.mean(
                best_scores
            )
        )


        max_best_similarity = float(
            np.max(
                best_scores
            )
        )


        min_best_similarity = float(
            np.min(
                best_scores
            )
        )


        # ----------------------------------------------------
        # Return threshold-free semantic evidence
        # ----------------------------------------------------

        return {
            "success": True,
            "status": "SENTENCE_ANSWER_EVIDENCE_READY",
            "question_id": question_id,
            "reference_role": reference_role,
            "reference_question": reference_question,

            "candidate_sentence_count":
                len(candidate_sentences),

            "reference_sentence_count":
                len(reference_sentences),

            "sentence_results":
                sentence_results,

            "mean_best_similarity":
                round(
                    mean_best_similarity,
                    4
                ),

            "max_best_similarity":
                round(
                    max_best_similarity,
                    4
                ),

            "min_best_similarity":
                round(
                    min_best_similarity,
                    4
                ),

            "reason": None
        }


# ============================================================
# DEVELOPMENT TEST
# ============================================================

def main():

    print("=" * 70)
    print("AEGIE TRUE SENTENCE-LEVEL MINILM TEST")
    print("=" * 70)


    evaluator = SentenceAnswerEvaluator()


    # --------------------------------------------------------
    # Development-only test.
    # This is NOT participant research data.
    # --------------------------------------------------------

    question_id = "CS_E02"


    test_answer = (
        "Authentication verifies the identity of a user. "
        "A password or another authentication factor can "
        "help verify who the user is. "
        "Authorization determines what an authenticated user "
        "is permitted to access or perform. "
        "For example, an administrator can have permissions "
        "that a normal user does not."
    )


    result = evaluator.evaluate(
        question_id=question_id,
        transcript=test_answer
    )


    print()
    print("Question ID:", question_id)
    print("Status:", result.get("status"))


    if not result.get("success"):

        print()

        print(
            "FAIL: Sentence-level evidence "
            "was not generated."
        )

        print(
            "Reason:",
            result.get("reason")
        )

        return


    print()

    print(
        "Reference role:",
        result.get("reference_role")
    )


    print(
        "Reference sentences:",
        result.get("reference_sentence_count")
    )


    print(
        "Candidate sentences:",
        result.get("candidate_sentence_count")
    )


    print()
    print("-" * 70)
    print("BEST MATCH FOR EACH REFERENCE SENTENCE")
    print("-" * 70)


    for item in result.get(
        "sentence_results",
        []
    ):

        print()

        print(
            "Reference sentence "
            f"{item['reference_sentence_number']}:"
        )

        print(
            item[
                "reference_sentence"
            ]
        )

        print(
            "Best candidate sentence:",
            item[
                "best_candidate_sentence"
            ]
        )

        print(
            "Similarity:",
            item[
                "best_similarity"
            ]
        )


    print()
    print("-" * 70)
    print("TRUE SENTENCE MINILM FEATURES")
    print("-" * 70)


    print(
        "Mean best similarity:",
        result.get(
            "mean_best_similarity"
        )
    )


    print(
        "Maximum best similarity:",
        result.get(
            "max_best_similarity"
        )
    )


    print(
        "Minimum best similarity:",
        result.get(
            "min_best_similarity"
        )
    )


    print()
    print("=" * 70)

    print(
        "PASS: TRUE SENTENCE-LEVEL "
        "MINILM EVIDENCE GENERATED"
    )

    print("=" * 70)


    print()
    print("Reference sentences were used.")
    print("key_concepts were NOT used.")
    print("No similarity threshold was applied.")
    print("No 1-5 AEGIE score was generated.")
    print("No human annotation label was used.")

    print(
        "Development reference knowledge only; "
        "expert review is required before final research use."
    )


# ============================================================
# RUN DEVELOPMENT TEST
# ============================================================

if __name__ == "__main__":

    main()