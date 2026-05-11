from django.core.management.base import BaseCommand
from quiz_app.models import Question

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
]

class Command(BaseCommand):
    help = 'Import questions from the hardcoded list'

    def handle(self, *args, **options):
        count = 0
        for q in questions:
            obj, created = Question.objects.get_or_create(
                chapter=q['chapter'],
                question_number=q['question_number'],
                defaults=q
            )
            if created:
                count += 1
                self.stdout.write(f'Created: {q["chapter"]} 第{q["question_number"]}題')
            else:
                self.stdout.write(f'Exists: {q["chapter"]} 第{q["question_number"]}題')

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} questions!'))