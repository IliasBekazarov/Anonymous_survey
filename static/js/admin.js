// Получение CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

let currentTab = 'ratings';
let ratingsData = [];
let questionsData = [];
let detailedData = null;

// Проверка статуса аутентификации
async function checkAuth() {
    try {
        const response = await fetch('/api/auth/status/');
        const data = await response.json();
        
        if (data.authenticated) {
            document.getElementById('login-page').classList.add('hidden');
            document.getElementById('dashboard').classList.remove('hidden');
            loadDashboardData();
        } else {
            document.getElementById('login-page').classList.remove('hidden');
            document.getElementById('dashboard').classList.add('hidden');
        }
    } catch (error) {
        console.error('Ошибка проверки аутентификации:', error);
        document.getElementById('login-page').classList.remove('hidden');
    }
}

// Вход
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('login-error');
    
    try {
        const response = await fetch('/api/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            checkAuth();
        } else {
            const data = await response.json();
            errorDiv.textContent = data.error || 'Неверные логин или пароль';
            errorDiv.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Ошибка входа:', error);
        errorDiv.textContent = 'Ошибка подключения к серверу';
        errorDiv.classList.remove('hidden');
    }
}

// Выход
async function handleLogout() {
    try {
        await fetch('/api/auth/logout/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            }
        });
        checkAuth();
    } catch (error) {
        console.error('Ошибка выхода:', error);
    }
}

// Загрузка данных дашборда
async function loadDashboardData() {
    try {
        const [ratingsRes, questionsRes, detailedRes] = await Promise.all([
            fetch('/api/statistics/ratings/'),
            fetch('/api/questions/'),
            fetch('/api/statistics/detailed/')
        ]);
        
        ratingsData = await ratingsRes.json();
        questionsData = await questionsRes.json();
        detailedData = await detailedRes.json();
        
        switchTab(currentTab);
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
    }
}

// Переключение табов
function switchTab(tabName) {
    currentTab = tabName;
    
    // Обновление стилей кнопок
    document.querySelectorAll('.tab-button').forEach(btn => {
        if (btn.dataset.tab === tabName) {
            btn.classList.add('border-indigo-600', 'text-indigo-600');
            btn.classList.remove('border-transparent', 'text-gray-500', 'hover:text-gray-700');
        } else {
            btn.classList.remove('border-indigo-600', 'text-indigo-600');
            btn.classList.add('border-transparent', 'text-gray-500', 'hover:text-gray-700');
        }
    });
    
    // Показ/скрытие содержимого
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.add('hidden');
    });
    document.getElementById(`tab-${tabName}`).classList.remove('hidden');
    
    // Загрузка контента
    if (tabName === 'ratings') {
        renderRatings();
    } else if (tabName === 'questions') {
        renderQuestions();
    } else if (tabName === 'results') {
        renderResults();
    }
}

// ============= РЕЙТИНГ ПРЕПОДАВАТЕЛЕЙ =============

function renderRatings() {
    const content = document.getElementById('ratings-content');
    
    if (!ratingsData || ratingsData.length === 0) {
        content.innerHTML = `
            <div class="text-center py-12">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mx-auto text-gray-400 mb-4"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                <p class="text-gray-500">Пока нет данных для отображения</p>
            </div>
        `;
        return;
    }
    
    const bestTeacher = ratingsData[0];
    const totalResponses = ratingsData.reduce((sum, t) => sum + t.total_responses, 0);
    const avgRating = ratingsData.reduce((sum, t) => sum + (t.average_rating * t.total_responses), 0) / totalResponses;
    const highestRating = Math.max(...ratingsData.map(t => t.average_rating));
    const teachersWithResponses = ratingsData.filter(t => t.total_responses > 0).length;
    
    content.innerHTML = `
        <!-- Лучший преподаватель -->
        ${bestTeacher.total_responses > 0 ? `
        <div class="bg-gradient-to-r from-yellow-50 to-yellow-100 border border-yellow-200 rounded-lg p-6 mb-6">
            <div class="flex items-center gap-4">
                <div class="bg-yellow-400 rounded-full p-4">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-yellow-800"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path><path d="M4 22h16"></path><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"></path><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"></path><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"></path></svg>
                </div>
                <div>
                    <h3 class="text-sm font-medium text-gray-600">Лучший преподаватель</h3>
                    <p class="text-2xl font-bold text-gray-800">${bestTeacher.name}</p>
                    <p class="text-gray-600">Средний балл: <span class="font-semibold">${bestTeacher.average_rating.toFixed(2)}</span> из 5</p>
                    <p class="text-sm text-gray-500">Получено ответов: ${bestTeacher.total_responses}</p>
                </div>
            </div>
        </div>
        ` : ''}
        
        <!-- Информация -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <p class="text-gray-700">Всего ответов получено: <span class="font-semibold">${totalResponses}</span></p>
        </div>
        
        <!-- График -->
        <div class="bg-white border rounded-lg p-6 mb-6">
            <canvas id="ratings-chart" height="400"></canvas>
        </div>
        
        <!-- Статистические карточки -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-green-50 border border-green-200 rounded-lg p-6">
                <div class="flex items-center gap-3">
                    <div class="bg-green-500 rounded-full p-3">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-white"><polyline points="20 6 9 17 4 12"></polyline></svg>
                    </div>
                    <div>
                        <p class="text-sm text-gray-600">Высший балл</p>
                        <p class="text-2xl font-bold text-gray-800">${highestRating.toFixed(2)}</p>
                    </div>
                </div>
            </div>
            
            <div class="bg-orange-50 border border-orange-200 rounded-lg p-6">
                <div class="flex items-center gap-3">
                    <div class="bg-orange-500 rounded-full p-3">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-white"><line x1="12" y1="20" x2="12" y2="10"></line><line x1="18" y1="20" x2="18" y2="4"></line><line x1="6" y1="20" x2="6" y2="16"></line></svg>
                    </div>
                    <div>
                        <p class="text-sm text-gray-600">Средний балл</p>
                        <p class="text-2xl font-bold text-gray-800">${avgRating.toFixed(2)}</p>
                    </div>
                </div>
            </div>
            
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <div class="flex items-center gap-3">
                    <div class="bg-blue-500 rounded-full p-3">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-white"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                    </div>
                    <div>
                        <p class="text-sm text-gray-600">Преподавателей оценено</p>
                        <p class="text-2xl font-bold text-gray-800">${teachersWithResponses}</p>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Создание графика
    setTimeout(() => {
        const ctx = document.getElementById('ratings-chart');
        if (ctx) {
            const sortedData = [...ratingsData].filter(t => t.total_responses > 0).sort((a, b) => b.average_rating - a.average_rating);
            
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: sortedData.map(t => t.short_name),
                    datasets: [{
                        label: 'Средний балл',
                        data: sortedData.map(t => t.average_rating),
                        backgroundColor: sortedData.map((t, i) => i === 0 ? '#F59E0B' : '#6366F1'),
                        borderRadius: 4
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const teacher = sortedData[context.dataIndex];
                                    return [
                                        `Средний балл: ${teacher.average_rating.toFixed(2)}`,
                                        `Всего ответов: ${teacher.total_responses}`
                                    ];
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            max: 5,
                            grid: {
                                display: true
                            }
                        },
                        y: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        }
    }, 100);
}

// ============= УПРАВЛЕНИЕ ВОПРОСАМИ =============

function renderQuestions() {
    const listDiv = document.getElementById('questions-list');
    
    if (!questionsData || questionsData.length === 0) {
        listDiv.innerHTML = '<p class="text-gray-500 text-center py-8">Нет вопросов</p>';
        return;
    }
    
    listDiv.innerHTML = questionsData.map(q => `
        <div class="bg-white border border-gray-200 rounded-lg p-4 hover:bg-blue-50 transition-colors duration-300">
            <div class="flex justify-between items-start">
                <div class="flex-1">
                    <span class="text-sm text-gray-500">Вопрос ${q.order}</span>
                    <p class="text-gray-800 mt-1">${q.text}</p>
                </div>
                <button onclick="deleteQuestion(${q.id})" class="ml-4 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors duration-300 text-sm">
                    Удалить
                </button>
            </div>
        </div>
    `).join('');
}

async function addQuestion(event) {
    event.preventDefault();
    
    const text = document.getElementById('new-question-text').value;
    
    try {
        const response = await fetch('/api/questions/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ text })
        });
        
        if (response.ok) {
            document.getElementById('new-question-text').value = '';
            loadDashboardData();
        } else {
            alert('Ошибка при добавлении вопроса');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка при добавлении вопроса');
    }
}

async function deleteQuestion(id) {
    if (!confirm('Вы уверены, что хотите удалить этот вопрос?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/questions/${id}/delete/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken
            }
        });
        
        if (response.ok) {
            loadDashboardData();
        } else {
            alert('Ошибка при удалении вопроса');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка при удалении вопроса');
    }
}

// ============= ТАБЛИЦА РЕЗУЛЬТАТОВ =============

function renderResults() {
    const content = document.getElementById('results-content');
    
    if (!detailedData || !detailedData.teachers || detailedData.teachers.length === 0) {
        content.innerHTML = `
            <div class="text-center py-12">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mx-auto text-gray-400 mb-4"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><path d="M3 9h18"></path><path d="M9 21V9"></path></svg>
                <p class="text-gray-500">Нет данных для отображения</p>
            </div>
        `;
        return;
    }
    
    const teachers = detailedData.teachers;
    const questions = detailedData.questions;
    
    // Создание таблицы
    let tableHTML = `
        <div class="overflow-x-auto border rounded-lg">
            <table class="w-full">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="sticky left-0 bg-gray-50 px-4 py-3 text-left text-sm font-semibold text-gray-700 border-r">Преподаватель</th>
    `;
    
    questions.forEach(q => {
        tableHTML += `<th class="px-4 py-3 text-center text-sm font-semibold text-gray-700 border-r" title="${q.text}">В${q.order}</th>`;
    });
    
    tableHTML += `
                        <th class="px-4 py-3 text-center text-sm font-semibold text-gray-700 border-r">Средний балл</th>
                        <th class="px-4 py-3 text-center text-sm font-semibold text-gray-700">Всего ответов</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    teachers.forEach((teacher, idx) => {
        const bgClass = idx % 2 === 0 ? 'bg-white' : 'bg-gray-50';
        tableHTML += `
            <tr class="${bgClass} hover:bg-blue-50 transition-colors duration-200">
                <td class="sticky left-0 ${bgClass} hover:bg-blue-50 px-4 py-3 text-sm font-medium text-gray-800 border-r">${teacher.name}</td>
        `;
        
        questions.forEach(q => {
            const qData = teacher.questions[`q${q.order}`];
            if (qData && qData.count > 0) {
                const badgeClass = 
                    qData.average >= 4.5 ? 'bg-green-100 text-green-800' :
                    qData.average >= 3.5 ? 'bg-blue-100 text-blue-800' :
                    qData.average >= 2.5 ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800';
                
                tableHTML += `
                    <td class="px-4 py-3 text-center text-sm border-r">
                        <span class="inline-block ${badgeClass} px-2 py-1 rounded font-semibold">
                            ${qData.average.toFixed(2)}
                        </span>
                        <div class="text-xs text-gray-500">(${qData.count})</div>
                    </td>
                `;
            } else {
                tableHTML += `<td class="px-4 py-3 text-center text-sm text-gray-400 border-r">-</td>`;
            }
        });
        
        // Средний балл и количество ответов
        if (teacher.total_responses > 0) {
            const avgBadgeClass = 
                teacher.overall_average >= 4.5 ? 'bg-green-100 text-green-800' :
                teacher.overall_average >= 3.5 ? 'bg-blue-100 text-blue-800' :
                teacher.overall_average >= 2.5 ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800';
            
            tableHTML += `
                <td class="px-4 py-3 text-center border-r">
                    <span class="inline-block ${avgBadgeClass} px-2 py-1 rounded font-semibold text-sm">
                        ${teacher.overall_average.toFixed(2)}
                    </span>
                </td>
                <td class="px-4 py-3 text-center text-sm font-medium">${teacher.total_responses}</td>
            `;
        } else {
            tableHTML += `
                <td class="px-4 py-3 text-center text-sm text-gray-400 border-r">-</td>
                <td class="px-4 py-3 text-center text-sm text-gray-400">0</td>
            `;
        }
        
        tableHTML += '</tr>';
    });
    
    tableHTML += `
                </tbody>
            </table>
        </div>
    `;
    
    // Расшифровка вопросов
    tableHTML += `
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-6">
            <h3 class="font-semibold text-gray-800 mb-3">Расшифровка вопросов:</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-700">
    `;
    
    questions.slice(0, 6).forEach(q => {
        tableHTML += `<p><strong>В${q.order}</strong> — ${q.text}</p>`;
    });
    
    tableHTML += `
            </div>
        </div>
    `;
    
    content.innerHTML = tableHTML;
}

// Экспорт в CSV
function exportCSV() {
    window.location.href = '/api/export/csv/';
}

// Инициализация
checkAuth();
