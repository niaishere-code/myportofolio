Nama : Rania Aqila

NPM : 2506623282

Kelas : PBP C

TUGAS 01
--- Refleksi ---
1. Ya, saya menggunakan dan menambahkan beberapa semantik HTML5, yang mana mencangkup:
- <nav> : membuat navigation bar di kanan atas untuk nantinya direct ke 5 halaman berbeda (Home, Journey, Work, Profile, Contact)
- <h2> : membuat text section title berupa "What I'm Passionate About" "What They Say About Me" "Connect With Me" agar by default tidak sebesar title nama, namun cukup untuk dihighlight karena secara hirearki di bawah <h1>
- <section> : memisahkan antar section, di page about me ini antara "What I'm Passionate About" "What They Say About Me", dan "Connect With Me"
- <img> : mencantumkan foto pribadi & logo media sosial
- <svg> : membuat bunga di belakang foto dan icon custom (Github, LinkedIn, Email, Medium) pada section "Connect With Me" dalam bentuk vector sehingga warnanya bisa mengikuti tema saat di-hover, tanpa perlu load file gambar eksternal
- <div> : container untuk membungkus beberapa komponen menjadi satu
- <span> : membungkus bagian teks kecil di dalam elemen lain yang sifatnya inline
- <article> : membungkus konten yang sifatnya berdiri sendiri dan berulang, seperti tiap card "passion" (Writing, Project Management, Business Cases) dan tiap card testimoni
- <header> dan <footer> : masing-masing untuk bagian navbar di paling atas dan bagian copyright di paling bawah halaman

Seluruh elemen semantik yang digunakan diatas telah cukup untuk membuat struktur halaman About Me dalam website saya, sehingga beberapa elemen lainnya tidak diperlukan seperti <aside> yang mana memiliki fungsi utama yang sama dengan <div>

2. Saya menggunakan tata letak baru berupa grid pada section "What They Say About Me" dimana terdapat perubahan dari menggunakan 3 box menjadi 2 box, awalnya saya terdapat kesulitan dalam mengatur ulang kembali width & height dari kedua box agar sesuai dengan space yang ada dimana di awal text testimoni yang saya masukkan juga overflow/melewati batas box sehingga saya meng-adjust kembali font sizenya. Untuk perubahan font size saya pun memutuskan menggunakan satuan px instead of rem (yang awal digunakan di template) sebagaimana dengan satuan yang lebih besar perubahan dapat lebih mendetail. Elemen yang harus diubah posisinya tentunya bagian utamanya seperti envelope atau kotak testimoni sehingga isi di dalamnya mengikutinya saja. 

3. Karena website masih static, maka setiap kali ada pembaruan data saya perlu untuk mengubahnya satu persatu di file index.html saya. Dengan keterbatasan ini, untuk iterasi proyek selanjutnya, fungsionalitas dinamis yang paling ingin saya siapkan adalah mengubah data pada testimoni menjadi berbasis model/database sehingga bisa diubah melalui form atau halaman admin, tanpa perlu mengedit HTML setiap kali ada perubahan, lalu bisa juga integrasikan sistem emailing instead of direct link mailto aja menjadi ada section dimana mereka bisa mengirimkan email langsung. 

--- AI Declaration ---
Saya menggunakan gen AI berupa Claude dengan tetap mengerjakan bagian besar dari projek ini dan memanfaatkan AI secara ethical, yakni:
1. Mencari referensi awal: Sebelum memulai memodifikasi template, saya mencari tahu berbagai bentuk web porto melalui situs https://www.awwwards.com/websites/portfolio/ untuk mencari tahu apa saya komponen umum yang ada pada website portofolio dan mencari tahu style design yang sesuai dengan yang saya sukai, saya pun juga membaca dokumentasi HTML & CSS pada https://www.w3schools.com/html/default.asp dan https://www.w3schools.com/css/default.asp untuk mencari tahu komponen-komponen HTML & CSS dan masing-masing kegunaannya
2. Membenarkan Color Palette: Sejak awal saya menggunakan CP dengan nuansa pink yang saya dapati dari https://coolors.co/palettes/trending namun, saya merasa warna yang saya gunakan dan integrasinya dalam website saya masih kurang pas sehingga saya meminta AI dengan prompt "recommend color palettenya gimana yang sesuai gabungin vibe web pleurat itu sm color palette yg udah di pake sekarang" sebagaimana website portofolio https://www.pleurat.com/ yang saya temukan melalui https://www.awwwards.com/websites/portfolio/ menjadi referensi utama saya dalam style design website portofolio saya, digabungkan dengan beberapa referensi yang saya jabarkan lainnya.
3. Membuat Design Wireframe: Saya mengerjakan wireframe saya 100% sendiri sebagaimana sketch yang dapat dilihat melalui(static/img/WIREFRAME-PROFILE.jpg), wireframe ini menjadi baseline awal saya dalam memodifikasi dan menambahkan ulang code html & css saya
4. Membuat envelope di section What I'm Passionate About: Saya menemukan website uiwomeninbusiness.com dan menggunakan section bagian core value sebagai referensi saya, awalnya saya mencoba membuat sendiri bagian kotak dan segitiga dari envelope, namun positioningnya menjadi berantakan sehingga saya meminta AI dengan prompt "bagaimana cara membenarkan envelope ini agar bisa kegabung dan membuka keatas"
5. Membuat kotak di section What They Say About Me: Setelah awal digenerate oleh AI, terdapat kekurangan berupa sizing kotak yang tidak sesuai dimana foto pemberi testimoni bentuknya juga kotak, kotak tulisannya yang satu ukurannya terlalu besar sedangkan yang lainyya terlalu kecil sehingga tidak konsisten, saya pun mengubah sendiri di bagian .testimonial-card di style.css dengan menetapkan height: 600px; dan width: 400px; lalu saya pun juga mengadjust ulang font testimonial menjadi 10px;
6. Penggunaan AI lainnya dilakukan untuk bug fixes ketika dibutuhkan, kerangka utama dari website tetap dibuat sendiri