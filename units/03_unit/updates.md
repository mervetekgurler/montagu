# Updating Your `montagu-letters` Environment

If you set up your environment more than a few days ago, you likely installed a broken version of `stanza`. This is not something you did wrong. It's an issue with how `stanza` resolves on Python 3.13. I thought that Python 3.14 was the problem but turns out we have to go back one more and use Python 3.12. The fix is to rebuild your environment with a few small changes.

Follow these steps in order. Don't skip the verification step at the end — it's the only way to know it actually worked.

---

## Step 1: Remove your old environment

Open a terminal and run:

```bash
conda deactivate
conda env remove -n montagu-letters
```
---

## Step 2: Replace your `environment.yml`

**If you haven't changed your local `environment.yml`:**

```bash
git pull origin main
```

**If you're not sure, or you already edited it while troubleshooting:**

Check first:

```bash
git status
```

If it lists `environment.yml` as modified, either discard your local changes and pull cleanly:

```bash
git checkout -- environment.yml
git pull origin main
```

OR

Open `environment.yml` in the project folder and replace its entire contents with the version below. The key changes from before:

- `python=3.13` → `python=3.12` (this is the actual fix — `stanza` depends on `torch`, and `torch` doesn't yet support 3.13)
- `stanza` is now pinned to a known-good version range instead of "whatever pip finds"
- Channels are simplified to just `conda-forge`

```yaml
name: montagu-letters
channels:
  - conda-forge
dependencies:
  - jupyter
  - matplotlib
  - seaborn
  - numpy<2.0
  - python=3.12
  - ipykernel
  - scikit-learn
  - nltk
  - gensim
  - pandas
  - python-dotenv
  - spacy
  - lxml
  - requests
  - beautifulsoup4
  - ipywidgets
  - cryptography
  - pip
  - pip:
      - google-genai
      - pypdf
      - wordcloud
      - tqdm
      - folium
      - stanza>=1.8,<2.0
```

Save the file.

---

## Step 3: Rebuild the environment

```bash
conda env create -f environment.yml
conda activate montagu-letters
python -m ipykernel install --user --name montagu-letters
```

This will take a few minutes. That's normal — it's downloading a lot of packages.

---

## Step 4: Verify it actually worked

This is the step people skip, and then come to office hours confused two days later. Don't skip it.

In a terminal (with `montagu-letters` activated), run:

```bash
python -c "import stanza; print(stanza.__file__); print(stanza.__version__)"
```

**What success looks like:**
- The version printed is something like `1.8.x`, `1.9.x`, `1.10.x`, or higher — anything starting with `1.` is good.
- The file path includes `montagu-letters` in it somewhere, confirming it's coming from this environment and not some other Python install on your machine.

**What failure looks like:**
- The version prints as `0.3`. If you see this, your old broken install is still active somewhere — see Troubleshooting below.
- `ModuleNotFoundError: No module named 'stanza'` — the environment didn't build correctly, or you're not actually inside it. Check that your terminal prompt shows `(montagu-letters)` before trying again.

---

## Step 5: Open the notebook with the right kernel

When you open the notebook in Jupyter, check the kernel selector in the top right. It needs to say **`montagu-letters`**, not `Python 3` or `base`. If it's wrong, use the kernel menu to switch it.

Then run this in your first notebook cell as a final check:

```python
import stanza
print(stanza.__version__)
```

If that prints a `1.x` version, you're good to go — proceed to the NER notebook.

---

## Troubleshooting

**`pip show stanza` still says `Version: 0.3` after rebuilding.**
This usually means an old environment is still active, or you have stanza installed globally outside of conda, and Python is finding that copy first. Run `which python` (Mac/Linux) or `where python` (Windows) and confirm the path includes `montagu-letters`. If it doesn't, your terminal isn't actually inside the right environment — re-run `conda activate montagu-letters`.

**The `conda env create` step fails partway through.**
Copy the exact error message and bring it to office hours or post it in the class channel. Don't try to "fix" it by installing things one at a time with pip while outside the yaml — that's how environments end up in inconsistent states that are harder to debug later.

**Everything looks right, but the notebook still can't find `stanza`.**
Almost always a kernel mismatch — see Step 5. The notebook can be pointed at a totally different Python install than the one you just fixed in your terminal.
