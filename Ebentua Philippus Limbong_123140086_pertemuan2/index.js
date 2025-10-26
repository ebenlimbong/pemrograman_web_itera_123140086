// ============ CLASS DEFINITION ============
        class Schedule {
            constructor(id, courseName, courseCode, day, startTime, endTime, room, lecturer, notes = '') {
                this.id = id;
                this.courseName = courseName;
                this.courseCode = courseCode;
                this.day = day;
                this.startTime = startTime;
                this.endTime = endTime;
                this.room = room;
                this.lecturer = lecturer;
                this.notes = notes;
                this.createdAt = new Date().toISOString();
            }

            getDisplayTime = () => `${this.startTime} - ${this.endTime}`;

            getFullInfo = () => `${this.courseName} (${this.courseCode}) - ${this.day} ${this.getDisplayTime()}`;
        }

        // ============ SCHEDULE MANAGER CLASS ============
        class ScheduleManager {
            constructor(storageKey = 'schedules') {
                this.storageKey = storageKey;
                this.schedules = this.loadFromStorage();
            }

            loadFromStorage = () => {
                const data = localStorage.getItem(this.storageKey);
                return data ? JSON.parse(data) : [];
            };

            saveToStorage = () => {
                localStorage.setItem(this.storageKey, JSON.stringify(this.schedules));
            };

            addSchedule = (schedule) => {
                this.schedules.push(schedule);
                this.saveToStorage();
                return schedule;
            };

            updateSchedule = (id, updatedData) => {
                const index = this.schedules.findIndex(s => s.id === id);
                if (index !== -1) {
                    this.schedules[index] = { ...this.schedules[index], ...updatedData };
                    this.saveToStorage();
                    return this.schedules[index];
                }
                return null;
            };

            deleteSchedule = (id) => {
                const index = this.schedules.findIndex(s => s.id === id);
                if (index !== -1) {
                    this.schedules.splice(index, 1);
                    this.saveToStorage();
                    return true;
                }
                return false;
            };

            getSchedules = () => this.schedules;

            getScheduleById = (id) => this.schedules.find(s => s.id === id);

            sortByDay = () => {
                const dayOrder = { 'Senin': 1, 'Selasa': 2, 'Rabu': 3, 'Kamis': 4, 'Jumat': 5, 'Sabtu': 6 };
                return [...this.schedules].sort((a, b) => {
                    const dayDiff = dayOrder[a.day] - dayOrder[b.day];
                    if (dayDiff !== 0) return dayDiff;
                    return a.startTime.localeCompare(b.startTime);
                });
            };
        }

        // ============ UI MANAGER ============
        class UIManager {
            constructor(manager) {
                this.manager = manager;
                this.form = document.getElementById('scheduleForm');
                this.container = document.getElementById('scheduleContainer');
                this.alertContainer = document.getElementById('alert-container');
                this.editingId = null;
                this.init();
            }

            init = () => {
                this.form.addEventListener('submit', (e) => this.handleFormSubmit(e));
                this.render();
            };

            handleFormSubmit = async (e) => {
                e.preventDefault();
                
                const formData = {
                    courseName: document.getElementById('courseName').value,
                    courseCode: document.getElementById('courseCode').value,
                    day: document.getElementById('day').value,
                    startTime: document.getElementById('startTime').value,
                    endTime: document.getElementById('endTime').value,
                    room: document.getElementById('room').value,
                    lecturer: document.getElementById('lecturer').value,
                    notes: document.getElementById('notes').value,
                };

                if (this.editingId) {
                    this.manager.updateSchedule(this.editingId, formData);
                    this.showAlert('Jadwal berhasil diperbarui!', 'success');
                    this.editingId = null;
                } else {
                    const schedule = new Schedule(
                        Date.now(),
                        formData.courseName,
                        formData.courseCode,
                        formData.day,
                        formData.startTime,
                        formData.endTime,
                        formData.room,
                        formData.lecturer,
                        formData.notes
                    );
                    this.manager.addSchedule(schedule);
                    this.showAlert('Jadwal berhasil ditambahkan!', 'success');
                }

                this.form.reset();
                this.render();
            };

            handleEdit = (id) => {
                const schedule = this.manager.getScheduleById(id);
                if (schedule) {
                    document.getElementById('courseName').value = schedule.courseName;
                    document.getElementById('courseCode').value = schedule.courseCode;
                    document.getElementById('day').value = schedule.day;
                    document.getElementById('startTime').value = schedule.startTime;
                    document.getElementById('endTime').value = schedule.endTime;
                    document.getElementById('room').value = schedule.room;
                    document.getElementById('lecturer').value = schedule.lecturer;
                    document.getElementById('notes').value = schedule.notes;
                    this.editingId = id;
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }
            };

            handleDelete = (id) => {
                if (confirm('Apakah Anda yakin ingin menghapus jadwal ini?')) {
                    this.manager.deleteSchedule(id);
                    this.showAlert('Jadwal berhasil dihapus!', 'success');
                    this.render();
                }
            };

            showAlert = (message, type) => {
                const alert = document.createElement('div');
                alert.className = `alert alert-${type}`;
                alert.textContent = message;
                this.alertContainer.innerHTML = '';
                this.alertContainer.appendChild(alert);
                setTimeout(() => alert.remove(), 3000);
            };

            render = () => {
                const schedules = this.manager.sortByDay();
                
                if (schedules.length === 0) {
                    this.container.innerHTML = `
                        <div class="empty-state">
                            <p>Belum ada jadwal. Tambahkan jadwal baru untuk memulai!</p>
                        </div>
                    `;
                } else {
                    this.container.innerHTML = schedules.map(schedule => `
                        <div class="schedule-item ${this.editingId === schedule.id ? 'editing' : ''}">
                            <div class="schedule-header">
                                <div>
                                    <div class="schedule-title">${schedule.courseName}</div>
                                    <div class="schedule-time">${schedule.day} • ${schedule.getDisplayTime()}</div>
                                </div>
                            </div>
                            <div class="schedule-details">
                                <strong>Kode:</strong> ${schedule.courseCode}<br>
                                <strong>Ruangan:</strong> ${schedule.room}<br>
                                <strong>Dosen:</strong> ${schedule.lecturer}
                                ${schedule.notes ? `<br><strong>Catatan:</strong> ${schedule.notes}` : ''}
                            </div>
                            <div class="schedule-actions">
                                <button class="btn-edit" onclick="uiManager.handleEdit(${schedule.id})">Edit</button>
                                <button class="btn-danger" onclick="uiManager.handleDelete(${schedule.id})">Hapus</button>
                            </div>
                        </div>
                    `).join('');
                }

                this.updateStats();
            };

            updateStats = () => {
                const schedules = this.manager.getSchedules();
                const today = new Date().toLocaleDateString('id-ID', { weekday: 'long' });
                const todayCount = schedules.filter(s => s.day === today).length;

                document.getElementById('totalSchedules').textContent = schedules.length;
                document.getElementById('todaySchedules').textContent = todayCount;
            };
        }

        // ============ INITIALIZATION ============
        const manager = new ScheduleManager();
        const uiManager = new UIManager(manager);

        // Demo data untuk testing (uncomment jika ingin)
        // const demoSchedules = [
        //     new Schedule(1, 'Pemrograman Web', 'CS101', 'Senin', '08:00', '10:00', 'Ruang 101', 'Dr. Budi', 'Bawa laptop'),
        //     new Schedule(2, 'Basis Data', 'CS102', 'Selasa', '10:00', '12:00', 'Ruang 102', 'Prof. Ani', ''),
        // ];
        // demoSchedules.forEach(s => manager.addSchedule(s));
        // uiManager.render();