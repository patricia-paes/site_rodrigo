(() => {
  'use strict';
  // Current WebMCP lives on document; retain compatibility with early navigator implementations.
  const registry = [document.modelContext, navigator.modelContext]
    .find(context => typeof context?.registerTool === 'function');
  if (!registry) {
    document.documentElement.dataset.agentTools = 'unsupported';
    return;
  }
  const lifecycle = new AbortController();
  let dataPromise;
  const data = () => dataPromise ??= fetch('/site-data.json', {cache: 'no-cache'})
    .then(response => {
      if (!response.ok) throw new Error('As informações públicas estão temporariamente indisponíveis.');
      return response.json();
    }).catch(error => { dataPromise = undefined; throw error; });
  const inputSchema = {
    type: 'object',
    properties: {business: {type: 'string', enum: ['personal_trainer', 'visionair']}},
    required: ['business'],
    additionalProperties: false
  };
  function validate(input) {
    if (!input || typeof input !== 'object' || Array.isArray(input) ||
        Object.keys(input).some(key => key !== 'business') ||
        !['personal_trainer', 'visionair'].includes(input.business)) {
      throw new Error('Informe business como personal_trainer ou visionair.');
    }
    return input.business;
  }
  const tools = [
    {
      name: 'get_business_information',
      description: 'Consulta os dados públicos de Rodrigo Victor: apresentação, contato, região de atendimento e páginas oficiais de personal trainer ou VISIONAIR. Não agenda nem envia mensagens.',
      inputSchema,
      annotations: {readOnlyHint: true},
      async execute(input) {
        const business = validate(input);
        const result = (await data()).businesses[business];
        return JSON.stringify(result);
      }
    },
    {
      name: 'list_services',
      description: 'Lista as modalidades de treinamento ou serviços de filmagem com drone publicados por Rodrigo Victor. Preços, horários e disponibilidade devem ser confirmados pelo WhatsApp.',
      inputSchema,
      annotations: {readOnlyHint: true},
      async execute(input) {
        const business = validate(input);
        const info = (await data()).businesses[business];
        return JSON.stringify({business: info.name, services: info.services, contact: info.contact, booking: info.booking});
      }
    }
  ];
  for (const tool of tools) {
    try {
      Promise.resolve(registry.registerTool(tool, {signal: lifecycle.signal}))
        .then(() => { document.documentElement.dataset.agentTools = 'registered'; })
        .catch(() => { document.documentElement.dataset.agentTools = 'registration-error'; console.warn('Não foi possível registrar uma ferramenta WebMCP.'); });
    } catch (_) { console.warn('WebMCP indisponível neste navegador.'); }
  }
  window.addEventListener('pagehide', event => { if (!event.persisted) lifecycle.abort(); }, {once: true});
})();
