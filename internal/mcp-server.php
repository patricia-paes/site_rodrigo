<?php
declare(strict_types=1);

// Public, read-only, stateless MCP over Streamable HTTP. No credentials or customer data.
if (!defined('SITE_ROOT') || !defined('SITE_URL')) { http_response_code(404); exit; }
const ORIGIN_URL = 'https://rodrigovictor.com.br';
const VERSIONS = ['2025-11-25', '2025-06-18', '2025-03-26'];
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
header('Vary: Origin');

function respond($payload, int $status = 200): void {
    http_response_code($status);
    if ($payload !== null) { echo json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES); }
    exit;
}
function fail($id, int $code, string $message, int $status = 200): void {
    respond(['jsonrpc' => '2.0', 'id' => $id, 'error' => ['code' => $code, 'message' => $message]], $status);
}
function success($id, $result): void { respond(['jsonrpc' => '2.0', 'id' => $id, 'result' => $result]); }
function documentJson(string $file) {
    $contents = file_get_contents(SITE_ROOT . '/' . $file);
    if ($contents === false) { fail(null, -32603, 'Public information unavailable.', 503); }
    $data = json_decode($contents);
    if (json_last_error() !== JSON_ERROR_NONE) { fail(null, -32603, 'Public information unavailable.', 503); }
    return $data;
}
function toolsList(): array {
    $schema = ['type' => 'object', 'properties' => ['business' => ['type' => 'string', 'enum' => array_keys(get_object_vars(documentJson('site-data.json')->businesses))]], 'required' => ['business'], 'additionalProperties' => false];
    $annotations = ['readOnlyHint' => true, 'destructiveHint' => false, 'idempotentHint' => true, 'openWorldHint' => false];
    return [
        ['name' => 'get_business_information', 'description' => 'Consulta as informações públicas e o contato desta área. Não agenda nem envia mensagens.', 'inputSchema' => $schema, 'annotations' => $annotations],
        ['name' => 'list_services', 'description' => 'Lista os serviços publicados nesta área, quando houver. Valores e disponibilidade são confirmados pelo contato oficial.', 'inputSchema' => $schema, 'annotations' => $annotations]
    ];
}
function resourcesList(): array {
    return [
        ['uri' => SITE_URL . '/llms.txt', 'name' => 'Guia do site', 'mimeType' => 'text/plain'],
        ['uri' => SITE_URL . '/index.md', 'name' => 'Apresentação desta área', 'mimeType' => 'text/markdown'],
        ['uri' => SITE_URL . '/site-data.json', 'name' => 'Dados públicos dos serviços', 'mimeType' => 'application/json']
    ];
}

$origin = $_SERVER['HTTP_ORIGIN'] ?? null;
if ($origin !== null && !in_array($origin, [ORIGIN_URL, 'https://www.rodrigovictor.com.br'], true)) {
    fail(null, -32000, 'Origin not allowed.', 403);
}
if ($origin !== null) { header('Access-Control-Allow-Origin: ' . $origin); }
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
if ($method === 'OPTIONS') {
    header('Access-Control-Allow-Methods: POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, MCP-Protocol-Version');
    respond(null, 204);
}
if ($method !== 'POST') {
    header('Allow: POST, OPTIONS');
    fail(null, -32000, 'Use MCP JSON-RPC via POST. This endpoint does not provide an SSE stream.', 405);
}
if (strtolower(trim(explode(';', $_SERVER['CONTENT_TYPE'] ?? '')[0])) !== 'application/json') {
    fail(null, -32600, 'Content-Type must be application/json.', 415);
}
$headerVersion = $_SERVER['HTTP_MCP_PROTOCOL_VERSION'] ?? '2025-03-26';
if (!in_array($headerVersion, VERSIONS, true)) { fail(null, -32600, 'Unsupported MCP protocol version.', 400); }
if ((int) ($_SERVER['CONTENT_LENGTH'] ?? 0) > 16384) { fail(null, -32600, 'Request too large.', 413); }
$raw = file_get_contents('php://input', false, null, 0, 16385);
if ($raw === false || strlen($raw) > 16384) { fail(null, -32600, 'Request too large.', 413); }
$request = json_decode($raw);
if (json_last_error() !== JSON_ERROR_NONE) { fail(null, -32700, 'Parse error.', 400); }
if (!is_object($request) || ($request->jsonrpc ?? '') !== '2.0' || !isset($request->method) || !is_string($request->method)) {
    fail(null, -32600, 'Invalid JSON-RPC request.', 400);
}
$hasId = property_exists($request, 'id');
$id = $request->id ?? null;
if ($hasId && !is_string($id) && !is_int($id)) { fail(null, -32600, 'Invalid request id.', 400); }
$params = $request->params ?? new stdClass();
if (!is_object($params)) { fail($id, -32602, 'Parameters must be an object.', 400); }
if (!$hasId) {
    if (strpos($request->method, 'notifications/') === 0) { respond(null, 202); }
    fail(null, -32600, 'Requests require an id.', 400);
}

switch ($request->method) {
    case 'initialize':
        if (!isset($params->protocolVersion) || !is_string($params->protocolVersion) || !isset($params->clientInfo) || !is_object($params->clientInfo) || !isset($params->capabilities) || !is_object($params->capabilities)) {
            fail($id, -32602, 'protocolVersion, clientInfo and capabilities are required.');
        }
        $card = documentJson('.well-known/mcp/server-card.json');
        success($id, [
            'protocolVersion' => in_array($params->protocolVersion, VERSIONS, true) ? $params->protocolVersion : VERSIONS[0],
            'capabilities' => $card->capabilities,
            'serverInfo' => ['name' => $card->name, 'version' => $card->version, 'title' => $card->title],
            'instructions' => 'Consulta somente informações públicas. Não há acesso a dados de clientes, preços em tempo real, agenda, reservas ou envio de mensagens. Confirme condições pelo contato oficial.'
        ]);
        break;
    case 'ping': success($id, new stdClass()); break;
    case 'tools/list': success($id, ['tools' => toolsList()]); break;
    case 'tools/call':
        if (!isset($params->name) || !is_string($params->name) || !in_array($params->name, ['get_business_information', 'list_services'], true)) { fail($id, -32602, 'Unknown tool.'); }
        $args = $params->arguments ?? new stdClass();
        if (!is_object($args) || !isset($args->business) || !is_string($args->business) || !in_array($args->business, array_keys(get_object_vars(documentJson('site-data.json')->businesses)), true) || count(get_object_vars($args)) !== 1) {
            fail($id, -32602, 'business must match a published identifier in this area; no additional arguments accepted.');
        }
        $data = documentJson('site-data.json');
        $business = $data->businesses->{$args->business};
        $result = $params->name === 'list_services' ? ['business' => $business->name, 'services' => $business->services, 'contact' => $business->contact, 'booking' => $business->booking] : $business;
        success($id, ['content' => [['type' => 'text', 'text' => json_encode($result, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)]], 'structuredContent' => $result, 'isError' => false]);
        break;
    case 'resources/list': success($id, ['resources' => resourcesList()]); break;
    case 'resources/templates/list': success($id, ['resourceTemplates' => []]); break;
    case 'resources/read':
        if (!isset($params->uri) || !is_string($params->uri)) { fail($id, -32602, 'A public resource URI is required.'); }
        foreach (resourcesList() as $resource) {
            if ($resource['uri'] === $params->uri) {
                $path = substr($resource['uri'], strlen(SITE_URL));
                $text = file_get_contents(SITE_ROOT . $path);
                if ($text === false) { fail($id, -32603, 'Resource unavailable.'); }
                success($id, ['contents' => [['uri' => $resource['uri'], 'mimeType' => $resource['mimeType'], 'text' => $text]]]);
            }
        }
        fail($id, -32002, 'Resource not found.');
        break;
    default: fail($id, -32601, 'Method not found.');
}
