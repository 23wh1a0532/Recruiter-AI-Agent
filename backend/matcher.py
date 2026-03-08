from backend.database import get_all_candidates


def calculate_score(candidate_skills, candidate_exp, required_skills, required_exp):

    # convert experience to integer
    candidate_exp = int(candidate_exp)

    # convert skills string to list
    candidate_skills = candidate_skills.lower().split(",")

    # skill match
    skill_match = len(set(candidate_skills).intersection(required_skills))

    if len(required_skills) == 0:
        skill_score = 0
    else:
        skill_score = skill_match / len(required_skills)

    # experience score
    if required_exp == 0:
        exp_score = 1
    else:
        exp_score = min(candidate_exp / required_exp, 1)

    total_score = (skill_score * 0.7) + (exp_score * 0.3)

    return round(total_score * 100, 2)


def rank_candidates(required_skills, required_exp):

    candidates = get_all_candidates()

    ranked_candidates = []

    for candidate in candidates:

        candidate_skills = candidate[2]
        candidate_exp = candidate[3]

        score = calculate_score(
            candidate_skills,
            candidate_exp,
            required_skills,
            required_exp
        )

        ranked_candidates.append({
            "email": candidate[1],
            "skills": candidate_skills,
            "experience": candidate_exp,
            "score": score
        })

    ranked_candidates.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked_candidates