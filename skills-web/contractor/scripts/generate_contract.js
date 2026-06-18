const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, VerticalAlign, PageNumber, PageBreak, TabStopType, TabStopPosition
} = require("docx");

// ============================================================
// FIXED DATA — Au Jardin d'Éole
// ============================================================
const PROPRIETAIRES = "Laetitia et Edouard PHELIP";
const ADRESSE_GITE = "Au Jardin d\u2019\u00C9ole \u2014 Chemin de Davidon, 97115 Sainte-Rose, Guadeloupe";
const CLASSEMENT = "Meubl\u00E9 de tourisme class\u00E9 3 \u00E9toiles";

const RIB = {
  titulaire: "M. ou Mme PHELIP Edouard ou L",
  banque: "BoursoBank",
  iban: "FR76 4061 8803 3200 0407 1771 179",
  bic: "BOUS FRPP XXX",
};

// ============================================================
// GUARANTEE CALCULATION LOGIC
// ============================================================
function calculateGuarantee(totalNet) {
  const RATE = 0.30;
  const MIN = 300;
  const MAX = 1500;
  const raw = totalNet * RATE;
  const rounded = Math.ceil(raw / 50) * 50; // round up to nearest 50€
  return Math.max(MIN, Math.min(MAX, rounded));
}

// ============================================================
// VARIABLE DATA — MODIFY THIS BLOCK FOR EACH CONTRACT
// ============================================================
// Claude: replace the values below with the collected reservation data.
// The rest of the script does not need modification.

const contract = {
  reference: "AJDE-2027-DUPUY",  // Format: AJDE-{STAY_YEAR}-{CLIENT_NAME_UPPER}
  client: {
    nom: "Famille DUPUY",              // Family name
    prenom_ref: "Fabienne et Didier DUPUY",  // Reference names for signature block
    email: "dupuy@example.com",
    // tel: "+33 6 12 34 56 78",       // Optional — uncomment if provided
  },
  sejour: {
    arrivee: "08/02/2027",     // DD/MM/YYYY
    depart: "15/02/2027",      // DD/MM/YYYY
    nuitees: 7,
    occupants: 12,
  },
  logements: [
    // Add/remove accommodation entries as needed
    { nom: "Kaz Aliz\u00E9", dates: "08/02 \u2192 15/02/2027", nuitees: 7, tarif: 150, soustotal: 1050 },
    { nom: "Souf Van", dates: "08/02 \u2192 15/02/2027", nuitees: 7, tarif: 115, soustotal: 805 },
    { nom: "Ti Briz", dates: "08/02 \u2192 15/02/2027", nuitees: 7, tarif: 80, soustotal: 560 },
  ],
  extras: [
    // { label, montant } — add/remove as needed
    { label: "Frais M\u00E9nage", montant: 150 },
    { label: "Taxe de s\u00E9jour", montant: 56 },
    { label: "Suppl\u00E9ment personne", montant: 140 },
  ],
  totalBrut: 2761,   // sum of sub-totals + extras
  remises: [
    // { label, montant } — leave empty array [] if no discounts
    { label: "Remise semaine (10%) + Remise exceptionnelle", montant: 441 },
  ],
  totalNet: 2320,     // totalBrut - sum of remises
  echeancier: [
    // Default: 30% / 30% / 40% — adjust percentages and dates
    { label: "Acompte (arrhes)", pct: "30%", montant: 696, date: "\u00C0 r\u00E9ception" },
    { label: "2\u1D49 versement", pct: "30%", montant: 696, date: "22 octobre 2026" },
    { label: "Solde", pct: "40%", montant: 928, date: "15 janvier 2027" },
  ],
  checkin: "15h00",     // default: 15h00
  checkout: "10h00",    // default: 10h00
  dateContrat: "27/03/2026",  // contract signature date (DD/MM/YYYY)
  // garantieOverride: null,  // Uncomment and set value to override auto-calculation
};

// Auto-calculate guarantee (or use override)
contract.garantie = contract.garantieOverride || calculateGuarantee(contract.totalNet);
console.log(`Guarantee: ${contract.garantie} EUR ${contract.garantieOverride ? '(manual override)' : `(auto: ${contract.totalNet} x 30%)`}`);

// ============================================================
// HELPERS
// ============================================================
// ============================================================
// PATHS — Adjust if assets are in a different location
// ============================================================
const path = require("path");
const SCRIPT_DIR = path.dirname(__filename);
const SKILL_DIR = path.resolve(SCRIPT_DIR, "..");
const LOGO_PATH = process.env.LOGO_PATH || path.join(SKILL_DIR, "assets", "Logo.png");
const SIGNATURE_PATH = process.env.SIGNATURE_PATH || path.join(SKILL_DIR, "assets", "Signature_Edouard.jpg");
const OUTPUT_DIR = process.env.OUTPUT_DIR || process.cwd();

const logoData = fs.readFileSync(LOGO_PATH);
const signatureData = fs.readFileSync(SIGNATURE_PATH);

const COLORS = {
  primary: "1B5E7B",
  secondary: "2E8B8B",
  accent: "E8A838",
  headerBg: "E8F4F8",
  altRow: "F7FAFB",
  text: "2C3E50",
  lightText: "5D6D7E",
  white: "FFFFFF",
};

const PAGE_WIDTH = 11906;
const MARGIN_LEFT = 1134;
const MARGIN_RIGHT = 1134;
const CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT;

const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };
const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: "D5D8DC" };
const thinBorders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };

function emptyPara(spacing = 100) {
  return new Paragraph({ spacing: { after: spacing }, children: [] });
}

function sectionTitle(text) {
  return new Paragraph({
    spacing: { before: 300, after: 150 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: COLORS.primary, space: 4 } },
    children: [
      new TextRun({ text, bold: true, size: 24, color: COLORS.primary, font: "Calibri" }),
    ],
  });
}

function bodyText(text, opts = {}) {
  return new Paragraph({
    spacing: { after: opts.after || 120, before: opts.before || 0 },
    alignment: opts.alignment || AlignmentType.JUSTIFIED,
    children: [
      new TextRun({ text, size: 21, color: COLORS.text, font: "Calibri", ...opts }),
    ],
  });
}

// Body paragraph with mixed formatting (bold + normal runs)
function bodyMixed(runs, opts = {}) {
  return new Paragraph({
    spacing: { after: opts.after || 120, before: opts.before || 0 },
    alignment: opts.alignment || AlignmentType.JUSTIFIED,
    children: runs.map(r => new TextRun({ size: 21, color: COLORS.text, font: "Calibri", ...r })),
  });
}

function makeCell(text, opts = {}) {
  const {
    bold = false, width, shading, alignment = AlignmentType.LEFT,
    fontSize = 20, color = COLORS.text, borders = thinBorders, colSpan
  } = opts;
  const cellOpts = {
    borders,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    verticalAlign: VerticalAlign.CENTER,
    children: [
      new Paragraph({
        alignment,
        children: [new TextRun({ text: String(text), bold, size: fontSize, color, font: "Calibri" })],
      }),
    ],
  };
  if (width) cellOpts.width = { size: width, type: WidthType.DXA };
  if (shading) cellOpts.shading = { fill: shading, type: ShadingType.CLEAR };
  if (colSpan) cellOpts.columnSpan = colSpan;
  return new TableCell(cellOpts);
}

// ============================================================
// BUILD DOCUMENT
// ============================================================

const headerContent = new Header({
  children: [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [
        new ImageRun({
          type: "png",
          data: logoData,
          transformation: { width: 280, height: 110 },
          altText: { title: "Logo", description: "Au Jardin d\u2019\u00C9ole", name: "logo" },
        }),
      ],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 40 },
      children: [
        new TextRun({ text: CLASSEMENT, size: 17, color: COLORS.lightText, font: "Calibri", italics: true }),
      ],
    }),
  ],
});

const footerContent = new Footer({
  children: [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 100 },
      border: { top: { style: BorderStyle.SINGLE, size: 1, color: COLORS.primary, space: 4 } },
      children: [
        new TextRun({ text: "Au Jardin d\u2019\u00C9ole \u2014 Chemin de Davidon, 97115 Sainte-Rose, Guadeloupe", size: 16, color: COLORS.lightText, font: "Calibri" }),
      ],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [
        new TextRun({ text: "Page ", size: 16, color: COLORS.lightText, font: "Calibri" }),
        new TextRun({ children: [PageNumber.CURRENT], size: 16, color: COLORS.lightText, font: "Calibri" }),
        new TextRun({ text: "/", size: 16, color: COLORS.lightText, font: "Calibri" }),
        new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, color: COLORS.lightText, font: "Calibri" }),
      ],
    }),
  ],
});

const children = [];

// ── TITLE ──
children.push(emptyPara(200));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 60 },
  children: [
    new TextRun({ text: "ACCORD DE R\u00C9SERVATION", bold: true, size: 36, color: COLORS.primary, font: "Calibri" }),
  ],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 40 },
  children: [
    new TextRun({ text: `R\u00E9f\u00E9rence : ${contract.reference}`, size: 20, color: COLORS.lightText, font: "Calibri" }),
  ],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 200 },
  children: [
    new TextRun({ text: "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500", size: 18, color: COLORS.accent }),
  ],
}));

// ── §1 PARTIES ──
children.push(sectionTitle("1. Parties"));
const partiesColW = Math.floor(CONTENT_WIDTH / 2);
children.push(new Table({
  width: { size: CONTENT_WIDTH, type: WidthType.DXA },
  columnWidths: [partiesColW, partiesColW],
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders: noBorders, width: { size: partiesColW, type: WidthType.DXA },
          children: [
            new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Les propri\u00E9taires :", bold: true, size: 21, color: COLORS.primary, font: "Calibri" })] }),
            new Paragraph({ spacing: { after: 30 }, children: [new TextRun({ text: PROPRIETAIRES, size: 21, color: COLORS.text, font: "Calibri" })] }),
            new Paragraph({ children: [new TextRun({ text: ADRESSE_GITE, size: 19, color: COLORS.lightText, font: "Calibri" })] }),
            new Paragraph({ spacing: { before: 30 }, children: [new TextRun({ text: "Email : aujardindeole@gmail.com", size: 19, color: COLORS.lightText, font: "Calibri" })] }),
            new Paragraph({ children: [new TextRun({ text: "T\u00E9l : +590 690 38 63 93", size: 19, color: COLORS.lightText, font: "Calibri" })] }),
          ],
        }),
        new TableCell({
          borders: noBorders, width: { size: partiesColW, type: WidthType.DXA },
          children: [
            new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Les locataires :", bold: true, size: 21, color: COLORS.primary, font: "Calibri" })] }),
            new Paragraph({ spacing: { after: 30 }, children: [new TextRun({ text: contract.client.nom, size: 21, color: COLORS.text, font: "Calibri" })] }),
            new Paragraph({ children: [new TextRun({ text: `Email : ${contract.client.email}`, size: 19, color: COLORS.lightText, font: "Calibri" })] }),
            ...(contract.client.tel ? [new Paragraph({ children: [new TextRun({ text: `T\u00E9l : ${contract.client.tel}`, size: 19, color: COLORS.lightText, font: "Calibri" })] })] : []),
          ],
        }),
      ],
    }),
  ],
}));

// ── §2 OBJET ──
children.push(sectionTitle("2. Objet"));
const nbLogements = contract.logements.length;
const logementsNoms = contract.logements.map(l => l.nom).join(", ");
children.push(bodyText(
  `Location de ${nbLogements} logement${nbLogements > 1 ? "s" : ""} (${logementsNoms}) au Jardin d\u2019\u00C9ole pour la p\u00E9riode du ${contract.sejour.arrivee} au ${contract.sejour.depart} (${contract.sejour.nuitees} nuit\u00E9es). Nombre d\u2019occupants d\u00E9clar\u00E9s : ${contract.sejour.occupants} personnes.`
));

// ── §3 DÉTAIL DE LA RÉSERVATION ──
children.push(sectionTitle("3. D\u00E9tail de la r\u00E9servation"));

const colWidths3 = [2400, 2200, 1000, 1600, 2438];
const headerRow3 = new TableRow({
  children: [
    makeCell("Logement", { bold: true, width: colWidths3[0], shading: COLORS.primary, color: "FFFFFF", fontSize: 19 }),
    makeCell("Dates", { bold: true, width: colWidths3[1], shading: COLORS.primary, color: "FFFFFF", fontSize: 19 }),
    makeCell("Nuit\u00E9es", { bold: true, width: colWidths3[2], shading: COLORS.primary, color: "FFFFFF", fontSize: 19, alignment: AlignmentType.CENTER }),
    makeCell("Tarif/nuit", { bold: true, width: colWidths3[3], shading: COLORS.primary, color: "FFFFFF", fontSize: 19, alignment: AlignmentType.RIGHT }),
    makeCell("Sous-total", { bold: true, width: colWidths3[4], shading: COLORS.primary, color: "FFFFFF", fontSize: 19, alignment: AlignmentType.RIGHT }),
  ],
});

const logementRows = contract.logements.map((l, i) => new TableRow({
  children: [
    makeCell(l.nom, { bold: true, width: colWidths3[0], shading: i % 2 === 1 ? COLORS.altRow : COLORS.white }),
    makeCell(l.dates, { width: colWidths3[1], shading: i % 2 === 1 ? COLORS.altRow : COLORS.white }),
    makeCell(String(l.nuitees), { width: colWidths3[2], shading: i % 2 === 1 ? COLORS.altRow : COLORS.white, alignment: AlignmentType.CENTER }),
    makeCell(`${l.tarif} \u20AC`, { width: colWidths3[3], shading: i % 2 === 1 ? COLORS.altRow : COLORS.white, alignment: AlignmentType.RIGHT }),
    makeCell(`${l.soustotal} \u20AC`, { width: colWidths3[4], shading: i % 2 === 1 ? COLORS.altRow : COLORS.white, alignment: AlignmentType.RIGHT }),
  ],
}));

const extraRows = contract.extras.map((e) => new TableRow({
  children: [
    makeCell(e.label, { bold: true, width: colWidths3[0] + colWidths3[1] + colWidths3[2] + colWidths3[3], colSpan: 4, shading: COLORS.altRow }),
    makeCell(`${e.montant} \u20AC`, { bold: true, width: colWidths3[4], shading: COLORS.altRow, alignment: AlignmentType.RIGHT }),
  ],
}));

const totalBrutRow = new TableRow({
  children: [
    makeCell("TOTAL BRUT", { bold: true, width: colWidths3[0] + colWidths3[1] + colWidths3[2] + colWidths3[3], colSpan: 4, shading: COLORS.headerBg }),
    makeCell(`${contract.totalBrut} \u20AC`, { bold: true, width: colWidths3[4], shading: COLORS.headerBg, alignment: AlignmentType.RIGHT }),
  ],
});

const remiseRows = contract.remises.map((r) => new TableRow({
  children: [
    makeCell(r.label, { width: colWidths3[0] + colWidths3[1] + colWidths3[2] + colWidths3[3], colSpan: 4, color: COLORS.secondary, fontSize: 19 }),
    makeCell(`- ${r.montant} \u20AC`, { width: colWidths3[4], color: COLORS.secondary, alignment: AlignmentType.RIGHT, fontSize: 19 }),
  ],
}));

const totalNetRow = new TableRow({
  children: [
    makeCell("TOTAL NET", { bold: true, width: colWidths3[0] + colWidths3[1] + colWidths3[2] + colWidths3[3], colSpan: 4, shading: COLORS.primary, color: "FFFFFF", fontSize: 22 }),
    makeCell(`${contract.totalNet} \u20AC`, { bold: true, width: colWidths3[4], shading: COLORS.primary, color: "FFFFFF", alignment: AlignmentType.RIGHT, fontSize: 22 }),
  ],
});

children.push(new Table({
  width: { size: CONTENT_WIDTH, type: WidthType.DXA },
  columnWidths: colWidths3,
  rows: [headerRow3, ...logementRows, ...extraRows, totalBrutRow, ...remiseRows, totalNetRow],
}));

// ── §4 ÉCHÉANCIER ──
children.push(sectionTitle("4. \u00C9ch\u00E9ancier de paiement"));

const colWidths4 = [3200, 1200, 2200, 3038];
const headerRow4 = new TableRow({
  children: [
    makeCell("\u00C9ch\u00E9ance", { bold: true, width: colWidths4[0], shading: COLORS.primary, color: "FFFFFF", fontSize: 19 }),
    makeCell("%", { bold: true, width: colWidths4[1], shading: COLORS.primary, color: "FFFFFF", fontSize: 19, alignment: AlignmentType.CENTER }),
    makeCell("Montant", { bold: true, width: colWidths4[2], shading: COLORS.primary, color: "FFFFFF", fontSize: 19, alignment: AlignmentType.RIGHT }),
    makeCell("Date limite", { bold: true, width: colWidths4[3], shading: COLORS.primary, color: "FFFFFF", fontSize: 19, alignment: AlignmentType.RIGHT }),
  ],
});

const echRows = contract.echeancier.map((e, i) => new TableRow({
  children: [
    makeCell(e.label, { bold: true, width: colWidths4[0], shading: i % 2 === 1 ? COLORS.altRow : COLORS.white }),
    makeCell(e.pct, { width: colWidths4[1], shading: i % 2 === 1 ? COLORS.altRow : COLORS.white, alignment: AlignmentType.CENTER }),
    makeCell(`${e.montant} \u20AC`, { bold: true, width: colWidths4[2], shading: i % 2 === 1 ? COLORS.altRow : COLORS.white, alignment: AlignmentType.RIGHT }),
    makeCell(e.date, { width: colWidths4[3], shading: i % 2 === 1 ? COLORS.altRow : COLORS.white, alignment: AlignmentType.RIGHT }),
  ],
}));

children.push(new Table({
  width: { size: CONTENT_WIDTH, type: WidthType.DXA },
  columnWidths: colWidths4,
  rows: [headerRow4, ...echRows],
}));

children.push(bodyText("Paiement par virement bancaire aux coordonn\u00E9es indiqu\u00E9es ci-dessous.", { before: 120, after: 60 }));

// ── §5 COORDONNÉES BANCAIRES ──
children.push(sectionTitle("5. Coordonn\u00E9es bancaires"));

const ribColW1 = 2600;
const ribColW2 = CONTENT_WIDTH - ribColW1;
const ribShading = COLORS.headerBg;

function ribRow(label, value) {
  return new TableRow({
    children: [
      makeCell(label, { bold: true, width: ribColW1, shading: ribShading, borders: thinBorders, fontSize: 20, color: COLORS.primary }),
      makeCell(value, { width: ribColW2, shading: COLORS.white, borders: thinBorders, fontSize: 20 }),
    ],
  });
}

children.push(new Table({
  width: { size: CONTENT_WIDTH, type: WidthType.DXA },
  columnWidths: [ribColW1, ribColW2],
  rows: [
    ribRow("Titulaire", RIB.titulaire),
    ribRow("Banque", RIB.banque),
    ribRow("IBAN", RIB.iban),
    ribRow("BIC / SWIFT", RIB.bic),
  ],
}));

// ── §6 DÉPÔT DE GARANTIE ──
children.push(sectionTitle("6. D\u00E9p\u00F4t de garantie"));

children.push(bodyMixed([
  { text: `Un d\u00E9p\u00F4t de garantie de ` },
  { text: `${contract.garantie} \u20AC`, bold: true },
  { text: ` est demand\u00E9 au locataire avant ou \u00E0 l\u2019arriv\u00E9e. Ce d\u00E9p\u00F4t peut \u00EAtre constitu\u00E9, au choix du locataire, par l\u2019un des moyens suivants :` },
]));

children.push(bodyMixed([
  { text: `\u2022 Par ch\u00E8que`, bold: true },
  { text: ` \u00E0 l\u2019ordre de Edouard PHELIP, remis \u00E0 l\u2019arriv\u00E9e. Le ch\u00E8que ne sera pas encaiss\u00E9 sauf en cas de d\u00E9gradations constat\u00E9es.` },
], { before: 60 }));

children.push(bodyMixed([
  { text: `\u2022 Par empreinte bancaire s\u00E9curis\u00E9e via Swikly`, bold: true },
  { text: ` (www.swikly.com). Un lien de paiement sera adress\u00E9 au locataire avant le s\u00E9jour. Aucun montant n\u2019est d\u00E9bit\u00E9 sauf en cas de d\u00E9gradations constat\u00E9es.` },
], { before: 20 }));

children.push(bodyText(
  "Le d\u00E9p\u00F4t de garantie est restitu\u00E9 (ou le ch\u00E8que rendu / l\u2019empreinte lib\u00E9r\u00E9e) dans un d\u00E9lai de 7 jours apr\u00E8s le d\u00E9part, sous r\u00E9serve de l\u2019absence de d\u00E9gradations constat\u00E9es lors de l\u2019\u00E9tat des lieux de sortie.",
  { before: 80 }
));

children.push(bodyMixed([
  { text: "En cas de d\u00E9gradations dont le co\u00FBt exc\u00E8de le montant du d\u00E9p\u00F4t de garantie, le locataire reste redevable du compl\u00E9ment.", bold: true },
  { text: " Les r\u00E9parations seront justifi\u00E9es par devis ou factures. \u00C0 d\u00E9faut d\u2019accord amiable, le propri\u00E9taire se r\u00E9serve le droit d\u2019engager les recours l\u00E9gaux n\u00E9cessaires." },
], { before: 80 }));

// ── §7 ASSURANCE ──
children.push(sectionTitle("7. Assurance"));

children.push(bodyMixed([
  { text: "Le locataire s\u2019engage \u00E0 fournir, avant son arriv\u00E9e ou au plus tard le jour du check-in, une " },
  { text: "attestation d\u2019assurance responsabilit\u00E9 civile", bold: true },
  { text: " (ou assurance vill\u00E9giature) couvrant les \u00E9ventuels dommages caus\u00E9s au logement et \u00E0 ses \u00E9quipements pendant la dur\u00E9e du s\u00E9jour." },
]));

children.push(bodyText(
  "En cas de sinistre d\u00E9passant le montant du d\u00E9p\u00F4t de garantie, l\u2019assurance du locataire sera sollicit\u00E9e en premier recours pour couvrir les frais de remise en \u00E9tat.",
  { before: 60 }
));

// ── §8 CONDITIONS D'ARRIVÉE / DÉPART + ÉTAT DES LIEUX ──
children.push(sectionTitle("8. Arriv\u00E9e, d\u00E9part et \u00E9tat des lieux"));

children.push(bodyText(`Arriv\u00E9e (check-in) : \u00E0 partir de ${contract.checkin}. D\u00E9part (check-out) : avant ${contract.checkout}. La remise des cl\u00E9s se fera sur place.`));

children.push(bodyMixed([
  { text: "Un " },
  { text: "\u00E9tat des lieux contradictoire", bold: true },
  { text: " sera r\u00E9alis\u00E9 \u00E0 l\u2019entr\u00E9e et \u00E0 la sortie du logement, en pr\u00E9sence des deux parties. Il sera accompagn\u00E9 de " },
  { text: "photographies dat\u00E9es", bold: true },
  { text: ". L\u2019\u00E9tat des lieux d\u2019entr\u00E9e servira de r\u00E9f\u00E9rence en cas de litige sur d\u2019\u00E9ventuelles d\u00E9gradations." },
], { before: 60 }));

// ── §9 CONDITIONS D'ANNULATION ──
children.push(sectionTitle("9. Conditions d\u2019annulation"));
children.push(bodyText("En cas d\u2019annulation par le locataire, l\u2019acompte vers\u00E9 restera acquis au propri\u00E9taire \u00E0 titre d\u2019arrhes."));
children.push(bodyText("En cas d\u2019annulation par le propri\u00E9taire, les sommes vers\u00E9es seront int\u00E9gralement rembours\u00E9es."));
children.push(bodyText("En cas de force majeure (catastrophe naturelle, pand\u00E9mie, etc.), les deux parties s\u2019engagent \u00E0 trouver un accord amiable (report des dates ou remboursement partiel/total)."));

// ── §10 ACCEPTATION ──
children.push(sectionTitle("10. Acceptation"));
children.push(bodyText("Le versement de l\u2019acompte vaut acceptation des pr\u00E9sentes conditions."));
children.push(bodyText("Une simple r\u00E9ponse par email avec la mention \u00AB lu et approuv\u00E9 \u00BB fait \u00E9galement office d\u2019accord."));

// ── §11 SIGNATURES ──
children.push(sectionTitle("11. Signatures"));

const sigColW = Math.floor(CONTENT_WIDTH / 2);
children.push(new Table({
  width: { size: CONTENT_WIDTH, type: WidthType.DXA },
  columnWidths: [sigColW, sigColW],
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders: noBorders, width: { size: sigColW, type: WidthType.DXA },
          children: [
            new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Les propri\u00E9taires :", bold: true, size: 21, color: COLORS.primary, font: "Calibri" })] }),
            new Paragraph({ spacing: { after: 30 }, children: [new TextRun({ text: PROPRIETAIRES, size: 21, color: COLORS.text, font: "Calibri" })] }),
            new Paragraph({
              spacing: { after: 30 },
              children: [
                new ImageRun({
                  type: "jpg",
                  data: signatureData,
                  transformation: { width: 160, height: 45 },
                  altText: { title: "Signature", description: "Signature propri\u00E9taire", name: "signature" },
                }),
              ],
            }),
            new Paragraph({ children: [new TextRun({ text: `Date : ${contract.dateContrat}`, size: 20, color: COLORS.text, font: "Calibri" })] }),
          ],
        }),
        new TableCell({
          borders: noBorders, width: { size: sigColW, type: WidthType.DXA },
          children: [
            new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Les locataires :", bold: true, size: 21, color: COLORS.primary, font: "Calibri" })] }),
            new Paragraph({ spacing: { after: 30 }, children: [new TextRun({ text: contract.client.prenom_ref, size: 21, color: COLORS.text, font: "Calibri" })] }),
            emptyPara(300),
            new Paragraph({ children: [new TextRun({ text: "Date : ______________________", size: 20, color: COLORS.text, font: "Calibri" })] }),
          ],
        }),
      ],
    }),
  ],
}));

// ============================================================
// ASSEMBLE DOCUMENT
// ============================================================
const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Calibri", size: 21, color: COLORS.text } },
    },
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 1800, right: MARGIN_RIGHT, bottom: 1134, left: MARGIN_LEFT },
        },
      },
      headers: { default: headerContent },
      footers: { default: footerContent },
      children,
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  // Generate filename from reference: AJDE-2027-DUPUY → Accord_Reservation_DUPUY_2027.docx
  const parts = contract.reference.split("-"); // ["AJDE", "2027", "DUPUY"]
  const clientName = parts.slice(2).join("_");
  const year = parts[1];
  const filename = `Accord_Reservation_${clientName}_${year}.docx`;
  const outPath = `${OUTPUT_DIR}/${filename}`;
  fs.writeFileSync(outPath, buffer);
  console.log("Contract generated: " + outPath);
});
