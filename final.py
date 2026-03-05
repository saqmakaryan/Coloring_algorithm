import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Lesson:
    def __init__(self, id, subject, teacher, group, is_half=False):
        self.id = id
        self.subject = subject
        self.teacher = teacher
        self.group = group
        self.is_half = is_half
        self.color = None
        self.neighbor_colors = set()

def are_conflicting(l1, l2):
    if l1.teacher == l2.teacher: return True
    p1, p2 = l1.group.split('_'), l2.group.split('_')
    if p1[1] == p2[1]:
        g1, g2 = p1[2], p2[2]
        if g1 == "Բոլոր" or g2 == "Բոլոր" or g1 == g2: return True
    return False

def solve_schedule_balanced(lessons, slots_per_day, days_count = 5):
    uncolored = list(range(len(lessons)))
    priority_colors = []
    for s in range(slots_per_day):
        for d in range(days_count):
            priority_colors.append(d * slots_per_day + s)

    while uncolored:
        curr = max(uncolored, key=lambda i: (len(lessons[i].neighbor_colors), 
                                             sum(1 for j in range(len(lessons)) if are_conflicting(lessons[i], lessons[j]))))
        chosen_color = next((c for c in priority_colors if c not in lessons[curr].neighbor_colors), None)
        if chosen_color is None:
            chosen_color = 0
            while chosen_color in lessons[curr].neighbor_colors: chosen_color += 1
                
        lessons[curr].color = chosen_color
        for i in range(len(lessons)):
            if are_conflicting(lessons[curr], lessons[i]):
                lessons[i].neighbor_colors.add(chosen_color)
        uncolored.remove(curr)

course_names = {1: "Մթ 540", 2: "Մթ 440", 3: "Մթ 340", 4: "Մթ 240"}
group_names = {1: "գործ 1", 2: "գործ 2", 3: "գործ 3"}

lessons = []
data = {
    1: [("ՄԱ", "Խոսրովյան"), ("ՀԼ", "Պետրոսյան", True), ("ԱԼ", "Մխիթարյան", True), ("Ֆ", "Մովսեսյան"), ("Ծր", "Սահակյան"), ("ՀՊ", "Բաղդասարյան", True)],
    2: [("ՄԱ", "Խոսրովյան"), ("ԴՀ", "Խոսրովյան"), ("OOP", "Սահակյան"), ("ՀԼ", "Պետրոսյան", True), ("ՌԼ", "Աղայան", True), ("ԱԼ", "Մխիթարյան", True)],
    3: [("ԿՏ", "Հովհաննիսյան"), ("ԾՏ", "Սահակյան"), ("ԴՄ", "Բադալյան"), ("ՄԾ", "Հովհաննիսյան"), ("ՀՏ և Վ", "Բադալյան"), ("ՄՖՀ", "Հայրապետյան")],
    4: [("ՕՀ", "Ղազարյան"), ("ՖԱ", "Հայրապետյան"), ("ՃՏ", "Ադոնց"), ("ՔՊ", "Խլոպուզյան", True), ("ԹՄ", "Բաբայան"), ("ՔԵ", "Բաբայան")]
}

for course_num, subjects in data.items():
    course_code = course_names[course_num]
    id_c = course_num * 100
    for sub, teacher, *half in subjects:
        is_h = half[0] if half else False
        lessons.append(Lesson(id_c, sub, teacher, f"Կ_{course_code}_Բոլոր", is_h))
        lessons.append(Lesson(id_c+1, sub, teacher, f"Կ_{course_code}_{group_names[1]}", is_h))
        lessons.append(Lesson(id_c+2, sub, teacher, f"Կ_{course_code}_{group_names[2]}", is_h))
        lessons.append(Lesson(id_c+3, sub, teacher, f"Կ_{course_code}_{group_names[3]}", is_h))
        id_c += 4

solve_schedule_balanced(lessons, 4)

slots_labels = ["I ԺԱՄ", "II ԺԱՄ", "III ԺԱՄ", "IV ԺԱՄ"]
days_labels = ["ԵՐԿՈՒՇԱԲԹԻ", "ԵՐԵՔՇԱԲԹԻ", "ՉՈՐԵՔՇԱԲԹԻ", "ՀԻՆԳՇԱԲԹԻ", "ՈՒՐԲԱԹ"]
1
for course_num, course_code in course_names.items():
    grid = pd.DataFrame("", index=slots_labels, columns=days_labels)
    course_data = [l for l in lessons if f"Կ_{course_code}" in l.group]
    
    for l in course_data:
        d_idx, s_idx = l.color // 4, l.color % 4
        if d_idx < 5 and s_idx < 4:
            tag = l.group.split('_')[-1]
            # Փոփոխված տրամաբանություն՝ առանց փակագծերի և «Դաս» նշումով
            display_tag = "Դաս" if tag == "Բոլոր" else tag
            info = f"{l.subject}\n{l.teacher}\n{display_tag}"
            
            if grid.iloc[s_idx, d_idx] == "":
                grid.iloc[s_idx, d_idx] = info
            else:
                grid.iloc[s_idx, d_idx] += "\n\n" + info

    plt.figure(figsize=(26, 16))
    sns.heatmap(pd.DataFrame(0, index=slots_labels, columns=days_labels), 
                annot=grid, fmt="", cmap=["#FFFFFF"], cbar=False, 
                linewidths=3, linecolor='black', 
                annot_kws={"size": 17, "weight": "bold", "color": "black"})
    
    plt.title(f"ԴԱՍԱՑՈՒՑԱԿ: ԿՈՒՐՍ {course_code}", fontsize=38, fontweight='bold', pad=50)
    plt.xticks(fontsize=22, fontweight='bold')
    plt.yticks(fontsize=22, fontweight='bold', rotation=0)
    
    for _, spine in plt.gca().spines.items():
        spine.set_linewidth(4)

    plt.tight_layout()
    plt.show()
    