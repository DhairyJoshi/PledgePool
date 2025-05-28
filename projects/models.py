from django.db import models
from django.utils.text import slugify
from accounts.models import pledgepool_user
from django.utils import timezone

def upload_cover(instance, filename):
    return f'projects/{instance.creator.username}/{instance.slug}/cover/{filename}'


def upload_gallery(instance, filename):
    return f'projects/{instance.creator.username}/{instance.slug}/gallery/{filename}'


class Campaign(models.Model):
    creator = models.ForeignKey(pledgepool_user, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    category = models.CharField(max_length=100)
    funding_goal = models.DecimalField(max_digits=12, decimal_places=2)
    achieved_funding = models.DecimalField(max_digits=12, decimal_places=2)
    total_pledges = models.IntegerField()
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    detailed_description = models.TextField()
    problem_statement = models.TextField()
    funds_use = models.TextField()

    campaign_cover = models.ImageField(upload_to=upload_cover, blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    # campaign_gallery = models.ImageField(upload_to=upload_gallery, blank=True, null=True)

    reward_title = models.CharField(max_length=255)
    reward_description = models.TextField()
    delivery = models.DateField()

    agreements = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            while Campaign.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class CampaignGalleryImage(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to=upload_gallery)

    def __str__(self):
        return f"Image for {self.campaign.title}"
    

class Pledge(models.Model):
    pledge_id = models.AutoField(primary_key=True)
    project = models.ForeignKey('Campaign', on_delete=models.CASCADE, related_name='pledges')
    backer = models.ForeignKey(pledgepool_user, on_delete=models.CASCADE, related_name='pledges_made')
    creator = models.ForeignKey(pledgepool_user, on_delete=models.CASCADE, related_name='pledges_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_pledged = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.backer.username} pledged ₹{self.amount} to {self.project.title} on {self.date_pledged.strftime('%Y-%m-%d')}"