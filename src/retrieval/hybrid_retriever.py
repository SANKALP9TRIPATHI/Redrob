"""
Hybrid retrieval.
"""


def hybrid_score(

    dense_score,

    capability_score
):

    return (

        0.7
        * dense_score

        + 0.3
        * capability_score
    )