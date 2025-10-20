let daftarTugasData = [];
let indexEdit = -1;

// Load data dari localStorage saat halaman dibuka
function loadData() {
    const data = localStorage.getItem('tugasMahasiswa');
    if (data) {
        daftarTugasData = JSON.parse(data);
    }
    tampilkanTugas();
    updateStatistik();
}

// Simpan data ke localStorage
function simpanData() {
    localStorage.setItem('tugasMahasiswa', JSON.stringify(daftarTugasData));
}

// Tampilkan notifikasi
function tampilkanNotifikasi(pesan, tipe) {
    const notif = document.getElementById('notifikasi');
    notif.textContent = pesan;
    notif.className = 'notifikasi ' + tipe;
    setTimeout(() => {
        notif.className = 'notifikasi';
    }, 3000);
}

// Handle submit form tambah tugas
document.getElementById('formTugas').addEventListener('submit', function(e) {
    e.preventDefault();

    const namaMahasiswa = document.getElementById('namaMahasiswa').value.trim();
    const mataKuliah = document.getElementById('mataKuliah').value.trim();
    const deskripsiTugas = document.getElementById('deskripsiTugas').value.trim();
    const deadline = document.getElementById('deadline').value;

    if (!namaMahasiswa || !mataKuliah || !deskripsiTugas || !deadline) {
        tampilkanNotifikasi('Semua field harus diisi!', 'error');
        return;
    }

    const tugas = {
        id: Date.now(),
        namaMahasiswa: namaMahasiswa,
        mataKuliah: mataKuliah,
        deskripsiTugas: deskripsiTugas,
        deadline: deadline,
        selesai: false
    };

    daftarTugasData.push(tugas);
    simpanData();
    tampilkanTugas();
    updateStatistik();
    tampilkanNotifikasi('Tugas berhasil ditambahkan!', 'success');
    document.getElementById('formTugas').reset();
});

// Tampilkan semua tugas
function tampilkanTugas() {
    const tbody = document.getElementById('daftarTugas');
    
    if (daftarTugasData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="no-data">Belum ada tugas ditambahkan</td></tr>';
        return;
    }

    tbody.innerHTML = '';
    daftarTugasData.forEach((tugas, index) => {
        const row = document.createElement('tr');
        const statusText = tugas.selesai ? 'Selesai' : 'Belum Selesai';
        const statusColor = tugas.selesai ? '#28a745' : '#dc3545';

        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${tugas.namaMahasiswa}</td>
            <td>${tugas.mataKuliah}</td>
            <td>${tugas.deskripsiTugas}</td>
            <td>${tugas.deadline}</td>
            <td><span style="color: ${statusColor}; font-weight: bold;">${statusText}</span></td>
            <td>
                <div class="action-buttons">
                    <button class="btn-ubah" onclick="bukaModalEdit(${index})">Ubah</button>
                    <button class="btn-hapus" onclick="hapusTugas(${index})">Hapus</button>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Buka modal edit
function bukaModalEdit(index) {
    indexEdit = index;
    const tugas = daftarTugasData[index];
    
    document.getElementById('editNamaMahasiswa').value = tugas.namaMahasiswa;
    document.getElementById('editMataKuliah').value = tugas.mataKuliah;
    document.getElementById('editDeskripsiTugas').value = tugas.deskripsiTugas;
    document.getElementById('editDeadline').value = tugas.deadline;
    
    document.getElementById('modalEdit').style.display = 'block';
}

// Tutup modal
function tutupModal() {
    document.getElementById('modalEdit').style.display = 'none';
    indexEdit = -1;
}

// Handle submit form edit
document.getElementById('formEdit').addEventListener('submit', function(e) {
    e.preventDefault();

    const namaMahasiswa = document.getElementById('editNamaMahasiswa').value.trim();
    const mataKuliah = document.getElementById('editMataKuliah').value.trim();
    const deskripsiTugas = document.getElementById('editDeskripsiTugas').value.trim();
    const deadline = document.getElementById('editDeadline').value;

    if (!namaMahasiswa || !mataKuliah || !deskripsiTugas || !deadline) {
        tampilkanNotifikasi('Semua field harus diisi!', 'error');
        return;
    }

    daftarTugasData[indexEdit].namaMahasiswa = namaMahasiswa;
    daftarTugasData[indexEdit].mataKuliah = mataKuliah;
    daftarTugasData[indexEdit].deskripsiTugas = deskripsiTugas;
    daftarTugasData[indexEdit].deadline = deadline;

    simpanData();
    tampilkanTugas();
    updateStatistik();
    tampilkanNotifikasi('Tugas berhasil diperbarui!', 'success');
    tutupModal();
});

// Hapus tugas
function hapusTugas(index) {
    if (confirm('Apakah Anda yakin ingin menghapus tugas ini?')) {
        daftarTugasData.splice(index, 1);
        simpanData();
        tampilkanTugas();
        updateStatistik();
        tampilkanNotifikasi('Tugas berhasil dihapus!', 'success');
    }
}

// Update statistik
function updateStatistik() {
    const total = daftarTugasData.length;
    const selesai = daftarTugasData.filter(t => t.selesai).length;
    const belum = total - selesai;

    document.getElementById('totalTugas').textContent = total;
    document.getElementById('tugasSelesai').textContent = selesai;
    document.getElementById('tugasBelum').textContent = belum;
}

// Tutup modal jika klik di luar
window.onclick = function(event) {
    const modal = document.getElementById('modalEdit');
    if (event.target == modal) {
        tutupModal();
    }
}

// Load data saat halaman dibuka
loadData();
