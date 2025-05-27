<?php
session_start();

// 模擬配置
define('SITE_TITLE', 'Python程式設計教學網站');
define('OPENAI_API_KEY', getenv('OPENAI_API_KEY'));

// 簡單路由系統
$page = $_GET['page'] ?? 'home';

function renderHeader($title = '') {
    $siteTitle = SITE_TITLE;
    $pageTitle = $title ? "$title - $siteTitle" : $siteTitle;
    
    echo "<!DOCTYPE html>
<html lang='zh-TW'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>$pageTitle</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <link href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css' rel='stylesheet'>
    <link href='static/css/style.css' rel='stylesheet'>
</head>
<body>
    <nav class='navbar navbar-expand-lg navbar-dark bg-primary fixed-top'>
        <div class='container'>
            <a class='navbar-brand' href='?page=home'>
                <i class='fas fa-code me-2'></i>Python 教學網站
            </a>
            <div class='navbar-nav ms-auto'>
                <a class='nav-link' href='?page=home'><i class='fas fa-home me-1'></i>首頁</a>
                <a class='nav-link' href='?page=lessons'><i class='fas fa-book me-1'></i>課程內容</a>
                <a class='nav-link' href='?page=ai-tutor'><i class='fas fa-robot me-1'></i>AI 助教</a>
                <a class='nav-link' href='?page=practice'><i class='fas fa-code me-1'></i>程式練習</a>
            </div>
        </div>
    </nav>
    <main class='main-content'>";
}

function renderFooter() {
    echo "</main>
    <footer class='bg-dark text-light py-4'>
        <div class='container'>
            <div class='row'>
                <div class='col-md-8'>
                    <h5>Python 程式設計教學網站</h5>
                    <p class='mb-0'>專為初學者設計的Python學習平台，結合AI助教提供個人化學習體驗。</p>
                </div>
                <div class='col-md-4 text-md-end'>
                    <p class='mb-0'>© 2024 Python教學網站. 版權所有.</p>
                </div>
            </div>
        </div>
    </footer>
    <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'></script>
    <script src='static/js/main.js'></script>
</body>
</html>";
}

// 路由處理
switch($page) {
    case 'home':
        renderHeader();
        include 'pages/home.php';
        break;
    case 'lessons':
        renderHeader('課程內容');
        include 'pages/lessons.php';
        break;
    case 'ai-tutor':
        renderHeader('AI 助教');
        include 'pages/ai_tutor.php';
        break;
    case 'practice':
        renderHeader('程式練習');
        include 'pages/practice.php';
        break;
    case 'api':
        // API 處理
        include 'api/handler.php';
        exit;
    default:
        renderHeader('404 - 頁面不存在');
        echo '<div class="container my-5 text-center">
                <h1>404 - 頁面不存在</h1>
                <a href="?page=home" class="btn btn-primary">返回首頁</a>
              </div>';
}

renderFooter();
?> 