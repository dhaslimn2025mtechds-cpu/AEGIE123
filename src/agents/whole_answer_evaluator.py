# ============================================================
# AEGIE WHOLE-ANSWER SEMANTIC EVALUATOR
# ============================================================
#
# Development semantic evidence component.
#
# Purpose:
# Compare the complete candidate transcript with the complete
# development reference_answer using MiniLM ONNX embeddings.
#
# IMPORTANT:
# - This produces ONE whole-answer cosine similarity.
# - It does NOT compare the transcript with individual concepts.
# - Similarity is semantic evidence only.
# - It is NOT a final 1-5 AEGIE score.
# - No pass/fail or adaptive threshold is applied here.
# - Development reference knowledge requires expert review
#   before final research use.
# ============================================================


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
# WHOLE ANSWER EVALUATOR
# ============================================================

class WholeAnswerEvaluator:

    def __init__(self):

        self.embedder = get_shared_minilm_embedder()


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
                "similarity": None,
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
                "similarity": None,
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
                "similarity": None,
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
                "similarity": None,
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
                "similarity": None,
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
                "similarity": None,
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
                "similarity": None,
                "reason": (
                    "Development reference_answer is empty."
                )
            }


        # ----------------------------------------------------
        # Encode WHOLE candidate + WHOLE reference in one batch
        # ----------------------------------------------------

        embeddings = self.embedder.encode(
            [
                transcript,
                reference_answer
            ]
        )


        candidate_embedding = embeddings[0]
        reference_embedding = embeddings[1]


        # ----------------------------------------------------
        # ONE whole-answer cosine similarity
        # ----------------------------------------------------

        similarity = cosine_similarity(
            candidate_embedding,
            reference_embedding
        )


        # ----------------------------------------------------
        # Return threshold-free semantic evidence
        # ----------------------------------------------------

        return {
            "success": True,
            "status": "WHOLE_ANSWER_EVIDENCE_READY",
            "question_id": question_id,
            "reference_role": reference_role,
            "reference_question": reference_question,
            "similarity": round(
                float(similarity),
                4
            ),
            "reason": None
        }


# ============================================================
# DEVELOPMENT TEST
# ============================================================

def main():

    print("=" * 70)
    print("AEGIE TRUE WHOLE-ANSWER MINILM TEST")
    print("=" * 70)


    evaluator = WholeAnswerEvaluator()


    # --------------------------------------------------------
    # Development-only test.
    #
    # CS_E02:
    # What is the difference between authentication
    # and authorization?
    #
    # This is not participant research data.
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
        print("FAIL: Whole-answer evidence was not generated.")
        print("Reason:", result.get("reason"))
        return


    print()
    print("Reference role:", result.get("reference_role"))
    print(
        "Whole MiniLM similarity:",
        result.get("similarity")
    )


    print()
    print("-" * 70)
    print("MEASUREMENT")
    print("-" * 70)

    print(
        "Complete candidate transcript "
        "<-> complete reference_answer"
    )

    print(
        "Number of whole-answer cosine similarities: 1"
    )


    print()
    print("=" * 70)
    print("PASS: TRUE WHOLE-ANSWER MINILM EVIDENCE GENERATED")
    print("=" * 70)

    print()
    print("No key-concept averaging was used.")
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