from pprint import pprint
from mistralai import Mistral
from django.conf import settings

def is_bad_review(
    review_text: str,
    api_key: str = settings.MISTRAL_API_KEY,
    grades: dict = settings.MISTRAL_MODERATIONS_GRADES,
) -> bool:
    client = Mistral(api_key=api_key)
    response = client.classifiers.moderate_chat(
        model="mistral-moderation-latest",
        inputs=[{"role": "user", "content": review_text}],
    )
    result = response.results[0].category_scores
    result = {key: round(value, 2) for key, value in result.items()}
    pprint(result)  # Для отладки (можно удалить)

    checked_result = {}
    for key, value in result.items():
        if key in grades:
            checked_result[key] = value >= grades[key]

    return any(checked_result.values())