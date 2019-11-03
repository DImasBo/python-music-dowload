from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

audio = MP3('dowload/Desiigner - Timmy Turner.mp3', ID3=ID3)


#audio.tags.delete(["dowload/Desiigner - Timmy Turner.mp3"], delete_v1=True, delete_v2=True) 
audio.tags.add(
    APIC(
     encoding=3, 
     mime='image/jpeg', 
     type=3, 
     desc=u'Cover', 
     data=open("1.jpg", 'rb').read() 
    ) 
)

audio.save("dowload/Desiigner - Timmy Turner.mp3", v2_version=3, v1=2) 