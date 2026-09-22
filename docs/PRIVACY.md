# Your data stays yours to manage

[По-русски](PRIVACY.ru.md)

Share the blank repository link. Keep your filled-in notebook, training history, photos, and health information out of the public repository and its issues or pull requests.

## Where to save personal information

- **Claude / ChatGPT:** a private project and a private backup on your device. Review your provider's data controls and workspace sharing settings.
- **Local folder:** `personal/`, which Git ignores. The blank templates live separately in `templates/`.

Git ignore rules prevent ordinary accidental additions of ignored files. They do not encrypt files, remove material already committed, stop someone using force-add, or control what an AI provider stores. A private project also does not mean an AI provider never processes or retains its contents.

There is no telemetry, account service, cloud database, or automatic upload in this repository. The optional Python helpers operate on local files. Uploading files to an AI app is a deliberate action you take in that app.

Only share information needed for coaching. A preferred name or nickname is enough. Full birth dates, addresses, employer details, identifying medical documents, and other people's records are unnecessary for onboarding. You may skip body measurements, food tracking, and health details.

## Before sharing repository changes

Run `python scripts/check_public.py` and inspect your changes. The checker rejects tracked private directories, unexpected public paths, common secret patterns, and stale or contaminated generated downloads. It cannot recognize every personal fact written into an otherwise public document. Human review is still necessary.

The starter builder uses an explicit list of public sources. It does not read `personal/`, chat exports, or neighboring directories. A blank template edited to contain personal details is still a potential leak: use a private copy.

If you accidentally publish private information, stop sharing the link and remove the exposed content, including repository history as needed. Rotate any exposed credentials. Removing a file in a later commit does not remove its earlier versions.
