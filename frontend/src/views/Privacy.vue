<script setup>
import { site } from '../config'
</script>

<template>
  <div class="legal">
    <div class="container legal-inner">
      <span class="eyebrow">Informativa</span>
      <h1>Privacy &amp; Cookie</h1>
      <p class="updated">Ai sensi del Regolamento UE 2016/679 (GDPR).</p>

      <h2>Titolare del trattamento</h2>
      <p>
        {{ site.companyName || site.name }} — {{ site.address.line1 }},
        {{ site.address.line2 }}. Email:
        <a :href="`mailto:${site.email}`">{{ site.email }}</a> · Tel:
        <a :href="`tel:${site.phone.tel}`">{{ site.phone.display }}</a>.
      </p>

      <h2>Quali dati raccogliamo</h2>
      <p>
        Quando effettui una prenotazione tramite il sito raccogliamo i dati che
        ci fornisci: <strong>nome, email, numero di telefono</strong>, data,
        orario, numero di persone ed eventuali piatti pre-ordinati.
      </p>

      <h2>Perché li usiamo</h2>
      <p>
        Esclusivamente per gestire e confermare la tua prenotazione e per
        contattarti in merito ad essa. La base giuridica è l'esecuzione di una
        tua richiesta (art. 6.1.b GDPR). Non usiamo i tuoi dati per marketing né
        li cediamo a terzi.
      </p>

      <h2>Per quanto tempo</h2>
      <p>
        I dati di prenotazione sono conservati per il tempo necessario alla
        gestione del servizio e poi rimossi.
      </p>

      <h2>Cookie</h2>
      <p>
        Il sito usa solo cookie/archiviazione locale tecnici, necessari al
        funzionamento (es. l'accesso dello staff). La pagina dei contatti può
        mostrare una <strong>mappa di Google</strong> che imposta cookie di
        terze parti: viene caricata soltanto dopo il tuo consenso tramite il
        banner cookie.
      </p>

      <h2>I tuoi diritti</h2>
      <p>
        Puoi chiedere in qualsiasi momento di accedere, correggere o cancellare
        i tuoi dati scrivendo a
        <a :href="`mailto:${site.email}`">{{ site.email }}</a>.
      </p>

      <router-link to="/" class="btn btn-ghost back">← Torna alla home</router-link>
    </div>
  </div>
</template>

<style scoped>
.legal {
  padding: 150px 0 var(--section);
}

.legal-inner {
  max-width: 760px;
}

.legal h1 {
  font-size: clamp(2.4rem, 5vw, 3.4rem);
  margin: 14px 0 8px;
}

.updated {
  color: var(--text-soft);
  font-size: 0.95rem;
  margin-bottom: 40px;
}

.legal h2 {
  font-size: 1.4rem;
  margin: 36px 0 12px;
}

.legal p {
  color: var(--text-soft);
  line-height: 1.8;
  font-size: 1.05rem;
}

.legal a {
  color: var(--primary);
  font-weight: 600;
}

.back {
  margin-top: 44px;
}
</style>
