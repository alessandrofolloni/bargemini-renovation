// ============================================================================
//  👉 DATI DEL LOCALE — MODIFICA QUI (e solo qui) i contatti reali del bar.
//  Tutto il sito (header, footer, home, prenotazioni) legge da questo file.
// ============================================================================

export const site = {
  name: 'Bar Gemini',
  tagline: 'Caffè · dal 1990',

  // Indirizzo
  address: {
    line1: 'Via Aristotele, 102',
    line2: '42122 Reggio Emilia (RE)',
    short: 'Via Aristotele 102, RE', // versione breve (card in home)
  },

  // Telefono — "display" è ciò che si vede, "tel" è per il link (solo cifre e +)
  phone: {
    display: '+39 0522 123456',
    tel: '+390522123456',
  },

  email: 'info@bargemini.it',

  // Social / link esterni (lascia '' per nasconderli)
  instagram: 'https://instagram.com/',

  // Link "Apri in Maps" e mappa incorporata in home.
  // Per aggiornare la mappa: Google Maps → Condividi → Incorpora una mappa →
  // copia SOLO l'indirizzo dentro src="..." e incollalo in mapEmbedUrl.
  mapsLink: 'https://maps.app.goo.gl/',
  mapEmbedUrl:
    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2830.826315254134!2d10.630018312061218!3d44.69255627095493!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x477fef6ea1a9e623%3A0xc0688a531d279774!2sVia%20Aristotele%2C%20102%2C%2042122%20Reggio%20Emilia%20RE!5e0!3m2!1sit!2sit!4v1706466000000!5m2!1sit!2sit',

  // Orari (giorno + orario). Lascia [] per non mostrarli.
  hours: [
    { days: 'Lun–Ven', time: '07:00 – 21:00' },
    { days: 'Sabato', time: '08:00 – 24:00' },
    { days: 'Domenica', time: 'Chiuso' },
  ],

  // Orario sintetico mostrato nella pagina prenotazioni
  hoursShort: 'Lun–Sab · 07:00 – 24:00',

  // Dati attività (obbligatori per legge in Italia) — comparirà nel footer
  vat: '', // es. 'P.IVA 01234567890'
  companyName: '', // es. 'Bar Gemini S.r.l.'
}
