# Panduan deploy model Hugging Face: `suratkiade`

Dokumen ini menjelaskan langkah-langkah ringkas untuk men-deploy model `suratkiade` dari Hugging Face agar dapat dipakai melalui **Hugging Face Spaces** (web app) atau **Inference Endpoints** (API produksi). Contoh di bawah menggunakan *Transformers* + *Gradio*.

## Opsi A — Deploy cepat via Hugging Face Spaces (Gradio)

1. **Siapkan akun & token**
   - Buat akun di Hugging Face.
   - Buat *Access Token* (Settings → Access Tokens) dengan scope **read**.

2. **Buat Space baru**
   - Klik **New Space** → pilih **Gradio**.
   - Nama Space misalnya `suratkiade-demo`.
   - Hardware bisa dimulai dari **CPU Basic**.

3. **Tambahkan file aplikasi**
   Buat file `app.py` dan `requirements.txt` di Space (via UI atau git clone).

   **app.py (contoh minimal)**
   ```python
   import gradio as gr
   from transformers import pipeline

   pipe = pipeline(
       task="text-generation",
       model="suratkiade",
   )

   def generate(prompt, max_new_tokens=200, temperature=0.7):
       output = pipe(
           prompt,
           max_new_tokens=max_new_tokens,
           temperature=temperature,
       )
       return output[0]["generated_text"]

   demo = gr.Interface(
       fn=generate,
       inputs=[
           gr.Textbox(label="Prompt"),
           gr.Slider(10, 500, value=200, step=10, label="Max New Tokens"),
           gr.Slider(0.1, 1.5, value=0.7, step=0.1, label="Temperature"),
       ],
       outputs=gr.Textbox(label="Output"),
       title="suratkiade Demo",
   )

   if __name__ == "__main__":
       demo.launch()
   ```

   **requirements.txt**
   ```text
   gradio
   transformers
   torch
   ```

4. **Deploy**
   - Commit file di Space (UI) atau `git push` jika memakai git clone.
   - Hugging Face akan otomatis build dan menjalankan Space.

5. **Uji**
   - Buka URL Space dan coba prompt sederhana.

## Opsi B — Deploy via Inference Endpoints (API produksi)

1. Buka halaman model `suratkiade` di Hugging Face.
2. Klik **Deploy → Inference Endpoints**.
3. Pilih cloud provider & instance.
4. Tunggu hingga status endpoint **Running**.
5. Gunakan endpoint URL + token untuk akses API.

## Catatan tambahan
- Jika model **private**, tambahkan token sebagai secret di Space (Settings → Secrets) dan gunakan `HUGGINGFACEHUB_API_TOKEN`.
- Untuk model besar, pertimbangkan GPU.
- Jika terjadi error `CUDA` atau *out of memory*, naikkan spesifikasi hardware atau turunkan `max_new_tokens`.

