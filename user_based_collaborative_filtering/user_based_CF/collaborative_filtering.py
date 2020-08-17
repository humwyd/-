from typing import Dict, List
from math import sqrt

class CF:

    def __init__(self,
                 data_dict: Dict[int, Dict[str, float]],
                 distance_method: str):
        distance_method_list = ["euclidean_distance", "manhattan_distance"]
        if distance_method not in distance_method_list:
            raise NameError("{} Not available.".format(distance_method))
        self.distance_method = distance_method
        self.pref_dict = data_dict

    def score(self, user_id_1: int, user_id_2: int) -> float:
        if user_id_1 not in self.pref_dict or user_id_2 not in self.pref_dict:
            return 0.0
        if self.distance_method == "euclidean_distance":
            return 1 / (1 + self.euclidean_distance(user_id_1, user_id_2))
        elif self.distance_method == "manhattan_distance":
            return 1 / (1 + self.manhattan_distance(user_id_1, user_id_2))

    def euclidean_distance(self, user_id_1: int, user_id_2: int) -> float:
        common_items = []
        for item in self.pref_dict[user_id_1]:
            if item in self.pref_dict[user_id_2]:
                common_items.append(item)
            else:
                continue
        if len(common_items) == 0:
            return 100.0
        return sqrt(sum([pow(self.pref_dict[user_id_1][common_item] - self.pref_dict[user_id_2][common_item], 2) for common_item in common_items]))

    def manhattan_distance(self, user_id_1: int, user_id_2: int) -> float:
        common_items = []
        for item in self.pref_dict[user_id_1]:
            if item in self.pref_dict[user_id_2]:
                common_items.append(item)
            else:
                continue
        if len(common_items) == 0:
            return 100.0
        return sum([self.pref_dict[user_id_1][common_item] + self.pref_dict[user_id_2][common_item] for common_item in common_items])

    def recommendation_res(self, target_user_id: int) -> List:
        if target_user_id not in self.pref_dict:
            raise NameError("{} is not a existed user ID.".format(target_user_id))
        total_score = {}
        score_len = {}
        for user in self.pref_dict:
            if user == target_user_id:
                continue
            faith = self.score(target_user_id, user)
            for item in self.pref_dict[user]:
                if item not in total_score:
                    total_score[item] = 0
                    score_len[item] = 0
                total_score[item] += (faith * self.pref_dict[user][item])
                score_len[item] += 1
        for item in total_score:
            total_score[item] /= score_len[item]
        total_score_sorted = sorted(total_score.items(), key=lambda x: x[1], reverse=True)
        return total_score_sorted

