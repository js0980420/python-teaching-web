<?php
/**
 * OpenAI API 整合類 (PHP版本)
 * 對應原本Flask的OpenAI功能
 */
class OpenAIHelper {
    private $api_key;
    private $api_url = 'https://api.openai.com/v1/chat/completions';
    
    public function __construct($api_key = null) {
        $this->api_key = $api_key ?: getenv('OPENAI_API_KEY');
    }
    
    /**
     * 與AI助教對話
     * 對應Flask的 /api/chat 端點
     */
    public function chatWithAI($user_message) {
        if (empty($this->api_key)) {
            throw new Exception('未設置OpenAI API金鑰');
        }
        
        if (empty($user_message)) {
            throw new Exception('請輸入訊息');
        }
        
        $data = [
            'model' => 'gpt-3.5-turbo',
            'messages' => [
                [
                    'role' => 'system',
                    'content' => '你是一個專業的Python程式設計助教。請用繁體中文回答，提供清楚的解釋和實用的程式碼範例。保持友善和耐心的教學態度。'
                ],
                [
                    'role' => 'user',
                    'content' => $user_message
                ]
            ],
            'max_tokens' => 1000,
            'temperature' => 0.7
        ];
        
        return $this->callOpenAI($data);
    }
    
    /**
     * 檢查Python程式碼
     * 對應Flask的 /api/check-code 端點
     */
    public function checkCode($code) {
        if (empty($this->api_key)) {
            throw new Exception('未設置OpenAI API金鑰');
        }
        
        if (empty($code)) {
            throw new Exception('請輸入程式碼');
        }
        
        $data = [
            'model' => 'gpt-3.5-turbo',
            'messages' => [
                [
                    'role' => 'system',
                    'content' => '你是一個Python程式碼檢查助手。請分析提供的程式碼，指出任何語法錯誤、邏輯問題或改進建議。用繁體中文回答。'
                ],
                [
                    'role' => 'user',
                    'content' => "請檢查這段Python程式碼：\n\n```python\n{$code}\n```"
                ]
            ],
            'max_tokens' => 800,
            'temperature' => 0.3
        ];
        
        return $this->callOpenAI($data);
    }
    
    /**
     * 調用OpenAI API的核心方法
     */
    private function callOpenAI($data) {
        $headers = [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $this->api_key
        ];
        
        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL => $this->api_url,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => json_encode($data),
            CURLOPT_HTTPHEADER => $headers,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_SSL_VERIFYPEER => false // 開發環境可用，生產環境建議移除
        ]);
        
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curl_error = curl_error($ch);
        curl_close($ch);
        
        if ($curl_error) {
            throw new Exception("cURL錯誤: {$curl_error}");
        }
        
        if ($http_code !== 200) {
            throw new Exception("API請求失敗，HTTP狀態碼: {$http_code}");
        }
        
        $decoded = json_decode($response, true);
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            throw new Exception("JSON解析錯誤: " . json_last_error_msg());
        }
        
        if (isset($decoded['error'])) {
            throw new Exception("OpenAI API錯誤: " . $decoded['error']['message']);
        }
        
        return $decoded['choices'][0]['message']['content'] ?? '無法獲取回應';
    }
}

/**
 * API端點處理器
 * 對應Flask的API路由
 */
class APIHandler {
    private $openai;
    
    public function __construct() {
        $this->openai = new OpenAIHelper();
    }
    
    public function handleRequest() {
        // 設定JSON回應標頭
        header('Content-Type: application/json; charset=utf-8');
        
        try {
            $action = $_GET['action'] ?? '';
            
            switch ($action) {
                case 'chat':
                    $this->handleChat();
                    break;
                case 'check-code':
                    $this->handleCheckCode();
                    break;
                default:
                    $this->sendError('無效的API端點', 400);
            }
        } catch (Exception $e) {
            $this->sendError($e->getMessage(), 500);
        }
    }
    
    private function handleChat() {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            $this->sendError('僅支援POST請求', 405);
            return;
        }
        
        $input = json_decode(file_get_contents('php://input'), true);
        $message = $input['message'] ?? '';
        
        $response = $this->openai->chatWithAI($message);
        $this->sendSuccess(['response' => $response]);
    }
    
    private function handleCheckCode() {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            $this->sendError('僅支援POST請求', 405);
            return;
        }
        
        $input = json_decode(file_get_contents('php://input'), true);
        $code = $input['code'] ?? '';
        
        $feedback = $this->openai->checkCode($code);
        $this->sendSuccess(['feedback' => $feedback]);
    }
    
    private function sendSuccess($data) {
        http_response_code(200);
        echo json_encode($data, JSON_UNESCAPED_UNICODE);
        exit;
    }
    
    private function sendError($message, $code = 400) {
        http_response_code($code);
        echo json_encode(['error' => $message], JSON_UNESCAPED_UNICODE);
        exit;
    }
}

// 使用範例
/*
// 在 api/handler.php 中使用：
require_once 'openai_helper.php';
$handler = new APIHandler();
$handler->handleRequest();
*/
?> 