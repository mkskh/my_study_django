from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# Create your models here.

def less_than_five(value):
    """Raire an error if the value is 5 or greater."""
    if value >= 5:
        raise ValidationError("The price must be lower than 5 euros.")



class Audio(models.Model):
    STYLES = (
        ('rock', 'Rock'),
        ('pop', 'Pop'),
        ('indie', 'Indie'),
        ('funky', 'Funky'),
        ('classic', 'Classic'),
        ('reggaeton', 'Reggaeton'),
        ('funky', 'Funky'),
    )
    AUDIO_TYPE = (
        ('song', 'Song'),
        ('podcast', 'Podcast'),
        ('effect', 'Effect'),
    )
    type = models.CharField(max_length=10, choices=AUDIO_TYPE)
    audio = models.FileField(upload_to='audio/', blank=False)
    title = models.CharField(max_length=250, blank=False)
    author = models.CharField(max_length=50, db_index=True, blank=True)
    author_website = models.URLField(blank=True)
    album = models.CharField(max_length=250, blank=True)
    duration = models.DurationField(blank=False)
    song_style = models.CharField(max_length=20, blank=True, choices=STYLES)
    playbacks = models.IntegerField(null=True, default=0, validators=[MinValueValidator(0)])
    price = models.DecimalField(null=False, decimal_places=2, max_digits=4, default=0.00)
    deal_of_the_day = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified =models.DateTimeField(auto_now=True)


    def clean(self):
        """Validate accross fields."""
        if self.type != "song" and self.song_style is not None:
            raise ValidationError("Only songs may have an associated style.")
        if self.price:
            if self.type == "song" and self.price >= 5:
                raise ValidationError("The price of a song must be lower than 5 euros.")
            if self.type == "podcast" and self.price >= 4:
                raise ValidationError("The price of a podcast must be lower than 4 euros.")
            if self.type == "effect" and self.price >= 95:
                raise ValidationError("The price of an audio effect must be lower than 100 euros.")
            

    def save(self, *args, **kwargs):
        '''Validation'''
        self.full_clean()
        super().save(*args, **kwargs)


        class Meta:
            constraints = [
                models.UniqueConstraint(fields=['title', 'author', 'album', 'duration'], name='unique_song')
            ]