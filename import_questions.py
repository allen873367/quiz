import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from quiz_app.models import Question
from django.core.files import File

# 圖片映射：根據章節和題號對應到圖片文件
image_mapping = {
    ('第7章　樹狀結構', 11): 'quiz_app/static/quiz_app/images/question_11.png',
    ('第7章　樹狀結構', 16): 'quiz_app/static/quiz_app/images/question_16.png',
}

questions = [
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 1,
        'question_text': '下列何種資料結構，經常用來表示階層式架構？',
        'option_a': '鏈結串列',
        'option_b': '堆疊',
        'option_c': '佇列',
        'option_d': '樹',
        'option_e': '雜湊表',
        'correct_answer': 'D'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 2,
        'question_text': '「樹」的資料結構中，若某節點沒有子節點，則稱為何？',
        'option_a': '根節點',
        'option_b': '內部節點',
        'option_c': '樹葉節點',
        'option_d': '兄弟節點',
        'option_e': None,
        'correct_answer': 'C'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 3,
        'question_text': '「樹」的資料結構中，某節點的所有子節點的個數稱為何？',
        'option_a': '階層 (Level)',
        'option_b': '高度 (Height)',
        'option_c': '深度 (Depth)',
        'option_d': '分支度 (Degree)',
        'option_e': '以上皆非',
        'correct_answer': 'D'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 4,
        'question_text': '「二元樹」中，每個節點最多可以有幾個子節點？',
        'option_a': '1',
        'option_b': '2',
        'option_c': '3',
        'option_d': '4',
        'option_e': '以上皆非',
        'correct_answer': 'B'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 5,
        'question_text': '若「二元樹」共有5 個節點，則二元樹的最小可能高度為何？',
        'option_a': '2',
        'option_b': '3',
        'option_c': '4',
        'option_d': '5',
        'option_e': '以上皆非',
        'correct_answer': 'B'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 6,
        'question_text': '若「二元樹」共有5 個節點，則二元樹的最大可能高度為何？',
        'option_a': '2',
        'option_b': '3',
        'option_c': '4',
        'option_d': '5',
        'option_e': '以上皆非',
        'correct_answer': 'D'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 7,
        'question_text': '若「二元樹」共有n個節點，則二元樹的最小可能高度為何？',
        'option_a': 'n',
        'option_b': 'log₂(n+1)',
        'option_c': '⌊log₂n⌋+1',
        'option_d': '⌈log₂(n+1)⌉',
        'option_e': '以上皆非',
        'correct_answer': 'D'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 8,
        'question_text': '一棵深度為5的「二元樹」，則最多可能的節點數為何？',
        'option_a': '32',
        'option_b': '31',
        'option_c': '64',
        'option_d': '63',
        'option_e': '以上皆非',
        'correct_answer': 'B'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 9,
        'question_text': '某「二元樹」的所有節點都只有左子樹，或都只有右子樹，則樹的名稱為何？',
        'option_a': '完整二元樹 (Complete Binary Tree)',
        'option_b': '完滿二元樹 (Full Binary Tree)',
        'option_c': '歪斜二元樹 (Skewed Binary Tree)',
        'option_d': '以上皆非',
        'option_e': None,
        'correct_answer': 'C'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 10,
        'question_text': '若有5個節點，則相異的「二元樹」共有幾種？',
        'option_a': '25',
        'option_b': '32',
        'option_c': '42',
        'option_d': '60',
        'option_e': '以上皆非',
        'correct_answer': 'C'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 11,
        'question_text': '給定下列的樹：請問這棵樹是不是「完整二元樹」？',
        'option_a': '是',
        'option_b': '否',
        'option_c': '不一定',
        'option_d': None,
        'option_e': None,
        'correct_answer': 'B',
        'sequence_group': 'tree_analysis'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 12,
        'question_text': '承上題，請問這棵樹是不是「完滿二元樹」？',
        'option_a': '是',
        'option_b': '否',
        'option_c': '不一定',
        'option_d': None,
        'option_e': None,
        'correct_answer': 'B',
        'sequence_group': 'tree_analysis'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 13,
        'question_text': '承上題，請問這棵樹是不是「二元搜尋樹」？',
        'option_a': '是',
        'option_b': '否',
        'option_c': '不一定',
        'option_d': None,
        'option_e': None,
        'correct_answer': 'B',
        'sequence_group': 'tree_analysis'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 14,
        'question_text': '下列何種資料結構，經常被用來實現「二元搜尋樹」？',
        'option_a': '陣列',
        'option_b': '鏈結串列',
        'option_c': '堆疊',
        'option_d': '佇列',
        'option_e': '以上皆非',
        'correct_answer': 'B'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 15,
        'question_text': '下列何者的走訪次序是「左子樹、根節點、右子樹」？',
        'option_a': '前序走訪',
        'option_b': '中序走訪',
        'option_c': '後序走訪',
        'option_d': '層序走訪',
        'option_e': '以上皆非',
        'correct_answer': 'B'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 16,
        'question_text': '下列何者為二元樹的前序走訪？',
        'option_a': 'F B A D C E G I H',
        'option_b': 'A B C D E F G H I',
        'option_c': 'A C E D B H I G F',
        'option_d': '以上皆非',
        'option_e': None,
        'correct_answer': 'A'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 17,
        'question_text': '下列的資料結構中，何者適合用來實現二元搜尋樹的「層序走訪」(Level-Order Traversal)？',
        'option_a': '陣列',
        'option_b': '鏈結串列',
        'option_c': '堆疊',
        'option_d': '佇列',
        'option_e': '以上皆非',
        'correct_answer': 'D'
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 18,
        'question_text': '給定「二元搜尋樹」，則下列何種走訪方式，形成「排序」結果？',
        'option_a': '前序走訪',
        'option_b': '中序走訪',
        'option_c': '後序走訪',
        'option_d': '層序走訪',
        'option_e': '以上皆非',
        'correct_answer': 'B'
    },
    # ===== 以下為自編新題目（第19~23題）=====
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 19,
        'question_text': '在「二元搜尋樹」(Binary Search Tree) 中進行搜尋操作，平均時間複雜度為何？在最差情況下（歪斜樹）又為何？',
        'option_a': 'O(log n)，O(n)',
        'option_b': 'O(n)，O(n²)',
        'option_c': 'O(1)，O(log n)',
        'option_d': 'O(n log n)，O(n)',
        'option_e': 'O(log n)，O(log n)',
        'correct_answer': 'A',
        'is_new': True,
        'source_note': '自行設計：二元搜尋樹搜尋效率分析，補充既有題目未涵蓋之時間複雜度主題',
        'explanation': '二元搜尋樹(BST)在平衡狀態下高度約為 log₂n，搜尋時每層比較一次，故平均時間複雜度為 O(log n)。但在最差情況下（歪斜樹），樹退化為鏈結串列，高度為 n，搜尋時間退化為 O(n)。',
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 20,
        'question_text': '下列關於二元樹的「後序走訪」(Postorder Traversal) 敘述何者正確？',
        'option_a': '走訪順序為：根節點 → 左子樹 → 右子樹',
        'option_b': '走訪順序為：左子樹 → 右子樹 → 根節點',
        'option_c': '走訪順序為：左子樹 → 根節點 → 右子樹',
        'option_d': '走訪順序為：右子樹 → 左子樹 → 根節點',
        'option_e': '以上皆非',
        'correct_answer': 'B',
        'is_new': True,
        'source_note': '自行設計：補充後序走訪之定義測驗，既有題目涵蓋前序與中序但未直接測驗後序',
        'explanation': '二元樹的三種基本走訪順序為：前序（根→左→右）、中序（左→根→右）、後序（左→右→根）。後序走訪先處理左子樹，再處理右子樹，最後才拜訪根節點。選項 A 為前序，選項 C 為中序。',
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 21,
        'question_text': '在資料結構中，將「二元樹」以陣列表示時，若父節點索引為 i，則其左子節點與右子節點索引分別為何？（索引從 1 開始）',
        'option_a': '左子節點 = 2i，右子節點 = 2i+1',
        'option_b': '左子節點 = 2i+1，右子節點 = 2i+2',
        'option_c': '左子節點 = i+1，右子節點 = i+2',
        'option_d': '左子節點 = i/2，右子節點 = i/2+1',
        'option_e': '以上皆非',
        'correct_answer': 'A',
        'is_new': True,
        'source_note': '自行設計：樹的陣列表示法，補充既有題目未涵蓋之實作細節',
        'explanation': '將二元樹以陣列儲存時，若根節點索引為 1，則左子節點索引為 2i，右子節點索引為 2i+1。此公式是陣列表示法的核心，也是堆積(Heap)實作的基礎。若索引從 0 開始，則左子為 2i+1，右子為 2i+2。',
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 22,
        'question_text': '關於「最小堆積」(Min-Heap) 的敘述，下列何者正確？',
        'option_a': '每個節點的值都大於其父節點的值',
        'option_b': '每個節點的值都大於其子節點的值',
        'option_c': '每個節點的值都小於或等於其子節點的值',
        'option_d': '樹中所有節點的值必須完全相同',
        'option_e': '最小堆積一定是完整二元樹',
        'correct_answer': 'C',
        'is_new': True,
        'source_note': '自行設計：堆積（Heap）為樹狀結構的重要應用，既有題目未涵蓋此主題',
        'explanation': '最小堆積(Min-Heap)的定義為：每個節點的值都小於或等於其子節點的值，因此根節點為全樹最小值。選項 A 描述的是最大堆積(Max-Heap)。選項 E 不正確，因為最小堆積不一定是完整二元樹，但通常實作成完整二元樹以利陣列儲存。',
    },
    {
        'chapter': '第7章　樹狀結構',
        'question_number': 23,
        'question_text': '關於「引線二元樹」(Threaded Binary Tree) 的敘述，下列何者正確？',
        'option_a': '將所有節點以鏈結串列方式儲存',
        'option_b': '利用空的鏈結欄位指向走訪的前驅或後繼節點',
        'option_c': '所有節點必須有兩個以上的子節點',
        'option_d': '只能用於完滿二元樹',
        'option_e': '引線二元樹無法進行走訪操作',
        'correct_answer': 'B',
        'is_new': True,
        'source_note': '自行設計：引線二元樹為進階二元樹主題，既有題目未涵蓋',
        'explanation': '引線二元樹(Threaded Binary Tree)的概念是：將二元樹中空的鏈結欄位（left 或 right 指標）加以利用，指向中序走訪的前驅或後繼節點。這樣可以在不使用堆疊或遞迴的情況下，高效地進行中序走訪，節省記憶體空間。',
    },
]

for q in questions:
    # 檢查是否有圖片
    image_path = image_mapping.get((q['chapter'], q['question_number']))
    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            file_obj = File(f, name=os.path.basename(image_path))
            q['question_image'] = file_obj

            # 使用update_or_create來更新已存在的記錄
            obj, created = Question.objects.update_or_create(
                chapter=q['chapter'],
                question_number=q['question_number'],
                defaults=q
            )
            if created:
                print(f'創建新題目: {q["chapter"]} 第{q["question_number"]}題')
            else:
                print(f'更新題目: {q["chapter"]} 第{q["question_number"]}題')
    else:
        # 使用update_or_create來更新已存在的記錄
        obj, created = Question.objects.update_or_create(
            chapter=q['chapter'],
            question_number=q['question_number'],
            defaults=q
        )
        if created:
            print(f'創建新題目: {q["chapter"]} 第{q["question_number"]}題')
        else:
            print(f'更新題目: {q["chapter"]} 第{q["question_number"]}題')

print(f'成功匯入 {len(questions)} 題！')