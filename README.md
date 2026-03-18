Gateway orchestrates: auth, routing, job creation, presigned URLs, metadata, policy.

Media service handles: upload/download, validation, hashing/dedup, virus scan if needed, transcoding/thumbnails, retention/deletion, access control enforcement, caching.

Workers do: inference only, reading media from object storage (or receiving already-preprocessed tensors/frames if you go that route).

workergpu199
198
4 x rtx 6000 blackwell
2 genoa 48 coeurs
1.5 TB

git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/victrolles/polymathic-inference-server.git
git push -u origin main

# TODO
faire une classe appart pour media_manager
faire qu'il ne charge pas des media deja chargé