import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


def less_than_five(value):
    """Raire an error if the value is 5 or greater."""
    if value >= 5:
        raise ValidationError("The price must be lower than 5 euros.")


def get_current_year():
    """Return the current year."""
    return datetime.datetime.today().year


class ValidatedModel(models.Model):
    """Automatically validate the model."""

    def save(self, *args, **kwargs):
        """Call validation on save."""
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        """Metadata."""

        abstract = True


class Author(ValidatedModel):
    """The Author model."""

    name = models.CharField(max_length=255)
    website = models.URLField(null=True, blank=True)
    first_appearance = models.SmallIntegerField(
        null=True, blank=True, verbose_name="Year of first appearance",
        validators=[MinValueValidator(1000), MaxValueValidator(get_current_year)]
    )
    last_appearance = models.SmallIntegerField(
        null=True, blank=True, verbose_name="Year of last appearance",
        validators=[MinValueValidator(1000), MaxValueValidator(get_current_year)]
    )

    def clean(self):
        """Validate the object."""
        if (self.first_appearance and self.last_appearance
                and self.first_appearance > self.last_appearance):
            raise ValidationError("The year of first appearance must be equal or "
                                  "lower to the year of last appearance.")


class Musician(ValidatedModel):
    """The Musician model."""

    INSTRUMENTS = (
        ("piano", "Piano"),
        ("eguitar", "Electric Guitar"),
        ("cguitar", "Classical Guitar"),
        ("aguitar", "Acoustic Guitar"),
        ("ebass", "Electric Bass"),
        ("bass", "Bass"),
        ("drums", "Drums"),
        ("voice", "Voice"),
        ("violin", "Violin"),
        ("harp", "Harp"),
        ("handpan", "Handpan"),
        ("tambourine", "Tambourine"),
        ("sax", "Saxophone"),
        ("trumpet", "Trumpet"),
        ("trombone", "Trombone"),
        ("flute", "Flute"),
        ("clarinet", "Clarinet"),
        ("ukulele", "Ukulele"),
    )

    name = models.CharField(max_length=150)
    nationality = models.CharField(max_length=2)
    instrument = models.CharField(max_length=25, choices=INSTRUMENTS)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="members")


class Album(ValidatedModel):
    """The Album model."""

    title = models.CharField(max_length=255)
    year_of_release = models.SmallIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(get_current_year)]
    )
    produced_by = models.CharField(max_length=255, null=True, blank=True)


class Song(ValidatedModel):
    """The Song model."""

    STYLES = (
        ("Indie", "Indie"),
        ("Pop", "Pop"),
        ("Rock", "Rock"),
        ("Funky", "Funky"),
        ("Reggaeton", "Reggaeton"),
        ("Classic", "Classic"),
        ("Orquestra", "Orquestra"),
        ("Folk", "Folk")
    )

    audio = models.FileField(upload_to="audio")
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL,
                               db_index=True, null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE,
                              max_length=250, null=True, blank=True)
    duration = models.DurationField()
    style = models.CharField(max_length=20, choices=STYLES, null=True, blank=True)
    playbacks = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=4, default=0,
                                validators=[less_than_five])
    deal_of_the_day = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='cr_by')
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='l_mod_by')


    class Meta:
        """Metadata."""

        constraints = [
            models.UniqueConstraint(fields=["title", "author", "album", "duration"],
                                    name="unique_song")
        ]

    def clean(self):
        User = get_user_model()
        if self.created_by_id is not None and not User.objects.filter(pk=self.created_by_id).exists():
            raise ValidationError("The created_by user does not exist.")
        
        if self.last_modified_by_id is not None and not User.objects.filter(pk=self.last_modified_by_id).exists():
            raise ValidationError("The last_modified_by user does not exist.")

        super().clean()
        
    # def clean(self):
    #     User = get_user_model()
    #     if self.created_by_id and not User.objects.filter(pk=self.created_by_id).exists():
    #         raise ValidationError("The created_by user does not exist.")

    #     if self.last_modified_by_id and not User.objects.filter(pk=self.last_modified_by_id).exists():
    #         raise ValidationError("The last_modified_by user does not exist.")

    #     super().clean()


class Profile(ValidatedModel):

    STYLES = (
        ("Indie", "Indie"),
        ("Pop", "Pop"),
        ("Rock", "Rock"),
        ("Funky", "Funky"),
        ("Reggaeton", "Reggaeton"),
        ("Classic", "Classic"),
        ("Orquestra", "Orquestra"),
        ("Folk", "Folk")
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='profile', null=True, blank=False)
    daily_start_time = models.TimeField(blank=False, default='09:00:00')
    daily_finish_time = models.TimeField(blank=False, default='14:00:00')
    preferred_style = models.CharField(max_length=30, choices=STYLES, blank=False, null=False)
    preferred_song = models.ForeignKey(Song, on_delete = models.SET_NULL, null=True, blank=True)

    class Meta:
        # Add a unique constraint to ensure each user has only one profile
        constraints = [
            models.UniqueConstraint(fields=["user"], name="unique_user_profile")
        ]


    def clean(self):
        # Check if a profile already exists for the user
        if self.pk is None and Profile.objects.filter(user=self.user).exists():
            raise ValidationError("A profile already exists for this user.")
        if not self.preferred_style:
            raise ValidationError({'preferred_style': 'Preferred style is required.'})
        super().clean()

# python manage.py test music.tests.task1