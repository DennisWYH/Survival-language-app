from django.db import models
from card.models import Card
from .word_grade import words_grade
from translator.models import TextTokenizer

# Let's use some statistics to determine the grade of a language text :)
class WordGradeByScience(models.Model):
    MAGIC_RECEIPES = [
        ("simple_magic", "The first simple algorism"),
    ]
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="ranking")
    algorism_name = models.CharField(max_length=50, choices=MAGIC_RECEIPES, default="")
    average_grade_number = models.FloatField(max_length=10, default="", blank=True)
    # average_grade_flag = models.FloatField(max_length=10, default="")
    token_grade_list = models.JSONField(default=dict, blank=True)

    # Some time fields never do harm
    creation_date = models.DateTimeField("date created", auto_now_add=True, blank=True)
    modification_date = models.DateTimeField("date modified",auto_now=True, blank=True)

    def __str__(self):
        return f"Card ID: {self.card.id}, Average Grade: {self.average_grade_number}, Token Grades: {self.token_grade_list}"

    def save(self, *args, **kwargs):
        tokenizer = TextTokenizer.objects.get(card=self.card)
        self.average_grade_number, self.token_grade_list = words_grade(tokenizer.tokens)
        super().save(*args, **kwargs)