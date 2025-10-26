from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from .models import Country
import os
from datetime import datetime, timezone

def generate_summary_image(path=None):
    if path is None:
        path = os.path.join(settings.BASE_DIR, 'cache', 'summary.png')
    os.makedirs(os.path.dirname(path), exist_ok=True)

    total = Country.objects.count()
    top5 = Country.objects.order_by('-estimated_gdp')[:5]
    timestamp = datetime.now(timezone.utc).isoformat()

   
    img = Image.new('RGB', (1200, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    title = f"Countries cached: {total}"
    d.text((20, 20), title, fill=(0,0,0))
    d.text((20, 60), f"Last refreshed: {timestamp}", fill=(0,0,0))
    y = 120
    d.text((20, 90), "Top 5 by estimated GDP:", fill=(0,0,0))
    for row in top5:
        d.text((20, y), f"{row.name} — {row.estimated_gdp:.2f}", fill=(0,0,0))
        y += 40

    img.save(path)
    return path
