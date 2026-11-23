<?php
declare(strict_types=1);

if (!isset($contentDirectory, $publicPath)) { http_response_code(404); exit; }
// Each entry point negotiates only its own HTML and Markdown.
function mediaQuality(string $accept, string $media): array {
    $quality = 0.0;
    $specificity = -1;
    foreach (explode(',', strtolower($accept)) as $entry) {
        $parts = array_map('trim', explode(';', $entry));
        $range = array_shift($parts);
        $rank = $range === $media ? 2 : ($range === 'text/*' ? 1 : ($range === '*/*' ? 0 : -1));
        if ($rank < 0) { continue; }
        $q = 1.0;
        foreach ($parts as $part) {
            if (preg_match('/^q\s*=\s*(.*)$/', $part, $m)) {
                $q = is_numeric($m[1]) ? max(0.0, min(1.0, (float) $m[1])) : 0.0;
            }
        }
        if ($rank > $specificity || ($rank === $specificity && $q > $quality)) {
            $quality = $q;
            $specificity = $rank;
        }
    }
    return [$quality, $specificity];
}

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
if (!in_array($method, ['GET', 'HEAD'], true)) {
    header('Allow: GET, HEAD');
    http_response_code(405);
    exit;
}
$accept = $_SERVER['HTTP_ACCEPT'] ?? '*/*';
[$mdQ, $mdRank] = mediaQuality($accept, 'text/markdown');
[$htmlQ] = mediaQuality($accept, 'text/html');
// Wildcards keep the normal HTML experience. Only an explicit preference selects Markdown.
$markdown = $mdRank === 2 && $mdQ > 0 && $mdQ >= $htmlQ;
header('Vary: Accept');
header('Cache-Control: no-cache');
$resourceBase = 'https://rodrigovictor.com.br' . $publicPath;
header('Link: <' . $resourceBase . '/llms.txt>; rel="describedby"; type="text/plain", <' . $resourceBase . '/index.md>; rel="alternate"; type="text/markdown", <' . $resourceBase . '/.well-known/mcp/server-card.json>; rel="service-desc"; type="application/mcp-server-card+json"');
header('X-Content-Type-Options: nosniff');
header('Content-Type: ' . ($markdown ? 'text/markdown' : 'text/html') . '; charset=utf-8');
if ($mdQ <= 0 && $htmlQ <= 0) {
    http_response_code(406);
    exit;
}
if ($markdown) { header('Content-Location: ' . $publicPath . '/index.md'); }
if ($method !== 'HEAD') { readfile($contentDirectory . ($markdown ? '/index.md' : '/index.html')); }
