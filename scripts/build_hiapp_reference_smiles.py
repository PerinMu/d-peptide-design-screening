#!/usr/bin/env python3
"""Build annotated SMILES and normalized citations for the hIAPP reference set.

The SMILES are computed from the curated sequence/modification annotations;
they are not copied from the source workbook. RDKit is used to parse,
stereochemically canonicalize, and validate the resulting structures.
"""

from __future__ import annotations

import argparse
import csv
import os
import tempfile
from pathlib import Path

try:
    from rdkit import Chem, rdBase
except ImportError as exc:  # pragma: no cover - exercised only without RDKit
    raise SystemExit(
        "RDKit is required. Install the pinned dependency with: "
        "python -m pip install -r requirements-reference-smiles.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
LITERATURE_CSV = ROOT / "targets/hiapp/data/reference/hiapp_literature_peptides.csv"
REFERENCES_CSV = ROOT / "targets/hiapp/data/designs/reference_inhibitor_sources.csv"


def ref(
    entry_ids: str,
    candidate_names: str,
    authors: str,
    title: str,
    publication: str,
    year: str,
    volume: str,
    issue: str,
    pages: str,
    doi_or_url: str,
    source_type: str = "primary_research_article",
    verification_status: str = "primary_doi_verified",
    curation_note: str = "",
) -> dict[str, str]:
    ref_id = f"HIAPP-REF-{len(REFERENCES) + 1:03d}"
    title = title.rstrip(".")
    if source_type == "sequence_database":
        citation = f"{authors} {title}. {publication}. {doi_or_url}"
    else:
        journal_part = f"{publication} {year}"
        if volume:
            journal_part += f";{volume}"
            if issue:
                journal_part += f"({issue})"
            if pages:
                journal_part += f":{pages}"
        citation = f"{authors} {title}. {journal_part}. {doi_or_url}"
    return {
        "reference_id": ref_id,
        "reference_entry_ids": entry_ids,
        "candidate_names": candidate_names,
        "authors": authors,
        "source_title": title,
        "publication": publication,
        "year": year,
        "volume": volume,
        "issue": issue,
        "pages_or_article": pages,
        "doi_or_url": doi_or_url,
        "source_type": source_type,
        "verification_status": verification_status,
        "curation_note": curation_note,
        "source_citation": citation,
    }


REFERENCES: list[dict[str, str]] = []


def add_ref(*args: str, **kwargs: str) -> None:
    REFERENCES.append(ref(*args, **kwargs))


add_ref("1-1", "NFGAIL", "Wang L, et al.", "A hIAPP-derived all-D-amino-acid inhibits hIAPP fibrillation efficiently at membrane surface by targeting α-helical oligomeric intermediates.", "FEBS Lett", "2014", "588", "6", "884-891", "https://doi.org/10.1016/j.febslet.2014.02.020")
add_ref("2-1;5-1", "NFGAILSS; SS", "UniProt Consortium.", "Human islet amyloid polypeptide (P10997).", "UniProtKB", "", "", "", "", "https://www.uniprot.org/uniprotkb/P10997", "sequence_database", "accession_verified", "The same UniProt record was cited in two source-workbook groups; merged here.")
add_ref("2-2;2-3", "QYGPILSS; NWGPILSS", "Rani S, et al.", "Synergistic effect of mutations in the amyloidogenic core of human amylin affords a new potent inhibitor of hAM fibrillation: computational design and experimental validation.", "ACS Chem Neurosci", "2026", "17", "3", "504-524", "https://doi.org/10.1021/acschemneuro.5c00433")
add_ref("3-1", "QBP1", "Ren B, et al.", "Amino acid sequence requirements of peptides that inhibit polyglutamine-protein aggregation and cell death.", "Biochem Biophys Res Commun", "2001", "288", "3", "703-710", "https://doi.org/10.1006/bbrc.2001.5783")
add_ref("4-1", "SNNFGA", "Scrocchi LA, et al.", "Design of peptide-based inhibitors of human islet amyloid polypeptide fibrillogenesis.", "J Mol Biol", "2002", "318", "3", "697-706", "https://doi.org/10.1016/S0022-2836(02)00164-X")
add_ref("4-2;4-3;4-4", "TNNWPL; TQNWAP; TQNWVP", "Rani S, et al.", "Modulation of hIAPP fibrillation by rationally designed hexapeptides revealed by molecular dynamics and experimental investigations.", "ACS Chem Neurosci", "2025", "16", "13", "2485-2501", "https://doi.org/10.1021/acschemneuro.5c00269")
add_ref("5-2;5-3;5-4;5-5", "SLS; LSLS; SNS; NSNS", "Zhang Q, et al.", "O-glycosylated peptides curtail the aggregation and toxicity of human islet amyloid polypeptide.", "Commun Biol", "2025", "8", "1", "1532", "https://doi.org/10.1038/s42003-025-08516-8")
add_ref("6-1", "dfPSMα3", "Kalitnik A, et al.", "Synthetic deformylated α-helical PSMα3 as a selective inhibitor of human amyloid aggregation", "Sci Rep", "2025", "15", "", "article 43071", "https://doi.org/10.1038/s41598-025-27115-5", "primary_research_article", "primary_doi_verified", "Corrected the source-workbook citation to the primary hIAPP study; the workbook had cited a related insulin-only paper.")
add_ref("7-1;7-2;7-3", "cyclo-CHVVGVI; cyclo-CDLGVFR; cyclo-CRCVFSG", "Yang L, et al.", "Rapid discovery of cyclic peptide protein aggregation inhibitors by continuous selection.", "Nat Chem Biol", "2025", "21", "4", "588-597", "https://doi.org/10.1038/s41589-024-01823-x", "primary_research_article", "primary_article_normalized_from_briefing", "The workbook cited a research briefing; this mapping points to the underlying primary article. The selected peptides are head-to-tail cyclized.")
add_ref("8-1", "C5", "Profit AA, et al.", "Peptide conjugates of benzene carboxylic acids as agonists and antagonists of amylin aggregation.", "Bioconjug Chem", "2017", "28", "2", "666-677", "https://doi.org/10.1021/acs.bioconjchem.6b00732")
add_ref("9-1;9-2", "HSSQN; HSSNQ", "Kaur H, Goyal B.", "In silico design and identification of new peptides for mitigating hIAPP aggregation in type 2 diabetes.", "J Biomol Struct Dyn", "2024", "42", "19", "10006-10021", "https://doi.org/10.1080/07391102.2023.2254411")
add_ref("10-1;10-2", "FGA-deltaF-L; FGA-deltaF-I", "Mishra A, et al.", "Conformationally restricted short peptides inhibit human islet amyloid polypeptide fibrillization.", "Chem Commun", "2013", "49", "26", "2688-2690", "https://doi.org/10.1039/c3cc38982k")
add_ref("11-1", "ANFLVH", "Potter KJ, et al.", "Amyloid inhibitors enhance survival of cultured human islets.", "Biochim Biophys Acta Gen Subj", "2009", "1790", "6", "566-574", "https://doi.org/10.1016/j.bbagen.2009.02.013")
add_ref("12-1;12-2;12-3;12-4;12-5;12-6;12-7;12-8;12-9", "AT; SA; KS; KT; KN; RF; cyclic-KS; cyclic-KN; cyclic-KT", "Mao X, et al.", "New peptide inhibitors modulate the self-assembly of islet amyloid polypeptide residues 11-20 in vitro.", "Eur J Pharmacol", "2017", "804", "", "102-110", "https://doi.org/10.1016/j.ejphar.2017.03.015")
add_ref("13-1", "IAPP-GI", "Yan LM, et al.", "Design of a mimic of nonamyloidogenic and bioactive human islet amyloid polypeptide as nanomolar affinity inhibitor of IAPP cytotoxic fibrillogenesis.", "Proc Natl Acad Sci USA", "2006", "103", "7", "2046-2051", "https://doi.org/10.1073/pnas.0507471103")
add_ref("14-1", "Pramlintide", "Kruger DF, Gloster MA.", "Pramlintide for the treatment of insulin-requiring diabetes mellitus: rationale and review of clinical data.", "Drugs", "2004", "64", "13", "1419-1432", "https://doi.org/10.2165/00003495-200464130-00003", "review", "review_doi_verified", "Review article; retained as the source-workbook citation and not treated as a primary peptide-design study.")
add_ref("15-1", "NYGAILSS", "Porat Y, et al.", "Inhibition of islet amyloid polypeptide fibril formation: a potential role for heteroaromatic interactions.", "Biochemistry", "2004", "43", "45", "14454-14462", "https://doi.org/10.1021/bi048582a")
add_ref("16-1", "I26P mutant", "Abedini A, et al.", "A single-point mutation converts the highly amyloidogenic human islet amyloid polypeptide into a potent fibrillization inhibitor.", "J Am Chem Soc", "2007", "129", "37", "11300-11301", "https://doi.org/10.1021/ja072157y")
add_ref("17-1", "rIAPP", "UniProt Consortium.", "Rat islet amyloid polypeptide (P12969).", "UniProtKB", "", "", "", "", "https://www.uniprot.org/uniprotkb/P12969", "sequence_database", "accession_verified")
add_ref("18-1;18-2;18-3", "Arg-1; Arg-2; Mem-T", "Patil SM, Alexandrescu AT.", "Charge-based inhibitors of amylin fibrillization and toxicity.", "J Diabetes Res", "2015", "2015", "", "article 946037", "https://doi.org/10.1155/2015/946037")
add_ref("19-1;19-2;19-3;19-4", "H18K-IAPP; H18R-IAPP; H18E-IAPP; H18A-IAPP", "Khemtémourian L, et al.", "Residue-specific effects of human islet amyloid polypeptide on self-assembly and cell toxicity.", "Biochimie", "2017", "142", "", "22-30", "https://doi.org/10.1016/j.biochi.2017.07.015")
add_ref("20-1;20-2", "Inhibitor-2; Inhibitor-3", "Heyl D, et al.", "Modeling the interface between islet amyloid polypeptide and insulin-based aggregation inhibitors: correlation to aggregation kinetics and membrane damage.", "J Chem Inf Model", "2012", "52", "5", "1298-1307", "https://doi.org/10.1021/ci300119c")
add_ref("21-1", "TK9", "Ghosh S, et al.", "Self-assembly of a nine-residue amyloid-forming peptide fragment of SARS coronavirus E-protein: mechanism of self-aggregation and amyloid inhibition of hIAPP.", "Biochemistry", "2015", "54", "13", "2249-2261", "https://doi.org/10.1021/acs.biochem.5b00061")
add_ref("22-1", "FLPNF", "Shi W, et al.", "A novel pentapeptide inhibitor reduces amyloid deposit formation by direct interaction with hIAPP.", "Int J Endocrinol", "2019", "2019", "", "article 9062032", "https://doi.org/10.1155/2019/9062032")
add_ref("23-1;23-2", "Tyr2; Tyr3", "Xin Q, et al.", "Oligotyrosines inhibit amyloid formation of human islet amyloid polypeptide in a tyrosine-number-dependent manner.", "ACS Biomater Sci Eng", "2019", "5", "2", "1092-1099", "https://doi.org/10.1021/acsbiomaterials.8b01384")
add_ref("24-1", "LA12", "Xuan W, et al.", "Monomer-targeting affinity peptide inhibitors of amyloid with no self-fibrillation and low cytotoxicity.", "Chem Commun", "2020", "56", "11", "1633-1636", "https://doi.org/10.1039/c9cc08671d")
add_ref("25-1;25-2", "SNNF(N-Me)GA(N-Me)ILSS; NF(N-Me)GA(N-Me)IL", "Kapurniotu A, et al.", "Structure-based design and study of nonamyloidogenic double N-methylated IAPP amyloid-core sequences as inhibitors of IAPP amyloid formation and cytotoxicity.", "J Mol Biol", "2002", "315", "3", "339-350", "https://doi.org/10.1006/jmbi.2001.5244")
add_ref("26-1;26-2;26-3", "IO8; N1-IO8; N2-IO8", "Obasse A, et al.", "Development of proteolytically stable N-methylated peptide inhibitors of aggregation of the amylin peptide implicated in type 2 diabetes.", "Interface Focus", "2017", "7", "6", "article 20160127", "https://doi.org/10.1098/rsfs.2016.0127")
add_ref("27-1;27-2;27-3", "WW2; WW4; YY2", "Huggins KNL, et al.", "Designed hairpin peptides interfere with amyloidogenesis pathways: fibril formation and cytotoxicity inhibition and interception of the preamyloid state.", "Biochemistry", "2011", "50", "38", "8202-8212", "https://doi.org/10.1021/bi200760h")
add_ref("28-1", "AP5", "Kellock J, et al.", "Peptides composed of alternating L- and D-amino acids inhibit amyloidogenesis in three distinct amyloid systems independent of sequence.", "J Mol Biol", "2016", "428", "11", "2317-2328", "https://doi.org/10.1016/j.jmb.2016.03.013")
add_ref("29-1;29-2;29-3", "Aib-NF-Aib-VHSS; Aib-NF-Aib-VH; Aib-NF-Aib-V", "Gilead S, Gazit E.", "Inhibition of amyloid fibril formation by peptide analogues modified with alpha-aminoisobutyric acid.", "Angew Chem Int Ed Engl", "2004", "43", "31", "4041-4044", "https://doi.org/10.1002/anie.200353565")
add_ref("30-1;30-2", "NFGAX2L; NFX2AX2L", "Paul A, et al.", "Disaggregation of amylin aggregate by conformationally restricted aminobenzoic-acid-containing alpha/beta and alpha/gamma hybrid peptidomimetics.", "Sci Rep", "2017", "7", "", "article 40095", "https://doi.org/10.1038/srep40095")
add_ref("31-1;31-2", "beta-cap-WW2; cyclo-WW2", "Sivanesam K, et al.", "Peptide inhibitors of the amyloidogenesis of IAPP: verification of the hairpin-binding geometry hypothesis.", "FEBS Lett", "2016", "590", "16", "2575-2583", "https://doi.org/10.1002/1873-3468.12261")
add_ref("32-1;32-2;32-3", "MCIP 2a; MCIP 2b; MCIP 2e", "Spanopoulou A, et al.", "Designed macrocyclic peptides as nanomolar amyloid inhibitors based on minimal recognition elements.", "Angew Chem Int Ed Engl", "2018", "57", "44", "14503-14508", "https://doi.org/10.1002/anie.201802979")
add_ref("33-1", "C14-RRRR-NH2", "Mao X, et al.", "Design and study of lipopeptide inhibitors for preventing aggregation of human islet amyloid polypeptide residues 11-20.", "J Pept Sci", "2018", "24", "1", "e3058", "https://doi.org/10.1002/psc.3058")
add_ref("34-1", "NCAM1-PrP", "Oh J, et al.", "Prion-protein-derived cell-penetrating peptide inhibits type II diabetes-associated islet amyloid polypeptide aggregation and cytotoxicity.", "Biochemistry", "2026", "65", "8", "1249-1260", "https://doi.org/10.1021/acs.biochem.5c00634")
add_ref("35-1;35-2;35-3", "TNGQ; MANT; YMSV", "Abioye RO, et al.", "Disaggregation of islet amyloid polypeptide fibrils as a potential antifibrillation mechanism of tetrapeptide TNGQ.", "Int J Mol Sci", "2022", "23", "4", "article 1972", "https://doi.org/10.3390/ijms23041972")


def structure(
    sequence: str,
    *,
    nterm: str | None = None,
    cterm: str | None = None,
    cyclic_backbone: bool = False,
    n_methylated: tuple[int, ...] = (),
    disulfide_pairs: tuple[tuple[int, int], ...] = (),
    glycosylation: tuple[tuple[int, str], ...] = (),
    note: str = "",
    structural_assumption: bool = False,
) -> dict[str, object]:
    nterm_assumed = nterm is None
    cterm_assumed = cterm is None
    return {
        "sequence": sequence,
        "nterm": nterm or "free",
        "cterm": cterm or "acid",
        "nterm_assumed": nterm_assumed,
        "cterm_assumed": cterm_assumed,
        "cyclic_backbone": cyclic_backbone,
        "n_methylated": set(n_methylated),
        "disulfide_pairs": tuple(disulfide_pairs),
        "glycosylation": dict(glycosylation),
        "note": note,
        "structural_assumption": structural_assumption,
    }


# Sequence letters use upper case for L residues and lower case for D residues.
# B = alpha-aminoisobutyric acid (Aib), X = alpha,beta-dehydrophenylalanine,
# and Z = 2-aminobenzoic acid (anthranilic acid).
SPECS: dict[str, dict[str, object]] = {
    "0001": structure("nfgail", note="All residues are encoded as D-amino acids according to the source record."),
    "0002": structure("NFGAILSS"),
    "0003": structure("QYGPILSS"),
    "0004": structure("NWGPILSS"),
    "0005": structure("WKWWPGIF"),
    "0006": structure("SNNFGA"),
    "0007": structure("TNNWPL"),
    "0008": structure("TQNWAP"),
    "0009": structure("TQNWVP"),
    "0010": structure("LANFLVHSSNNFGAIL"),
    "0011": structure("LANFLVHSSNNFGAIL", glycosylation=((7, "Glc"),), note="O-glucose attached at source-reported Ser19; anomeric stereochemistry is unspecified in the source.", structural_assumption=True),
    "0012": structure("LANFLVHSSNNFGAIL", glycosylation=((7, "Glc"), (8, "Glc")), note="O-glucose attached at source-reported Ser19 and Ser20; anomeric stereochemistry is unspecified in the source.", structural_assumption=True),
    "0013": structure("LANFLVHSSNNFGAIL", glycosylation=((7, "GlcNAc"),), note="O-GlcNAc attached at source-reported Ser19; anomeric stereochemistry is unspecified in the source.", structural_assumption=True),
    "0014": structure("LANFLVHSSNNFGAIL", glycosylation=((7, "GlcNAc"), (8, "GlcNAc")), note="O-GlcNAc attached at source-reported Ser19 and Ser20; anomeric stereochemistry is unspecified in the source.", structural_assumption=True),
    "0015": structure("MEFVAKLFKFFKDLLGKFLGNN", nterm="free", cterm="amide", note="The cited hIAPP study specifies deformylated PSMalpha3 with a free N-terminal amine and C-terminal amide."),
    "0016": structure("CHVVGVI", cyclic_backbone=True, cterm="cyclic", note="Represented as head-to-tail backbone-cyclized, as in the primary selection study."),
    "0017": structure("CDLGVFR", cyclic_backbone=True, cterm="cyclic", note="Represented as head-to-tail backbone-cyclized, as in the primary selection study."),
    "0018": structure("CRCVFSG", cyclic_backbone=True, cterm="cyclic", note="Represented as head-to-tail backbone-cyclized, as in the primary selection study."),
    "0019": structure("NFGAILSS", nterm="pyromellitate", note="Represented as N-terminally coupled to one pyromellitic-acid carboxyl; the source does not specify protonation, so the remaining carboxyls are neutral acids.", structural_assumption=True),
    "0020": structure("HSSQN"),
    "0021": structure("HSSNQ"),
    "0022": structure("FGAXL", note="X denotes alpha,beta-dehydrophenylalanine; E/Z alkene geometry is not specified in the source.", structural_assumption=True),
    "0023": structure("FGAXI", note="X denotes alpha,beta-dehydrophenylalanine; E/Z alkene geometry is not specified in the source.", structural_assumption=True),
    "0024": structure("ANFLVH"),
    "0025": structure("AMVGT", nterm="acetyl", cterm="amide"),
    "0026": structure("SSVMA", nterm="acetyl", cterm="amide"),
    "0027": structure("KFSFK", nterm="acetyl", cterm="amide"),
    "0028": structure("KFTFK", nterm="acetyl", cterm="amide"),
    "0029": structure("KFNFK", nterm="acetyl", cterm="amide"),
    "0030": structure("RFTFR", nterm="acetyl", cterm="amide"),
    "0031": structure("CKFSFKGSGKFSFKC", nterm="acetyl", disulfide_pairs=((0, 14),), note="The source labels this cysteine-ended peptide as cyclized; represented as a Cys-Cys disulfide macrocycle.", structural_assumption=True),
    "0032": structure("CKFNFKGSGKFNFKC", nterm="acetyl", disulfide_pairs=((0, 14),), note="The source labels this cysteine-ended peptide as cyclized; represented as a Cys-Cys disulfide macrocycle.", structural_assumption=True),
    "0033": structure("CKFTFKGSGKFTFKC", nterm="acetyl", disulfide_pairs=((0, 14),), note="The source labels this cysteine-ended peptide as cyclized; represented as a Cys-Cys disulfide macrocycle.", structural_assumption=True),
    "0034": structure("KCNTATCATQRLANFLVHSSNNF GAILSSTNVGSNTY".replace(" ", ""), cterm="amide", n_methylated=(23, 25), disulfide_pairs=((1, 6),), note="Mature hIAPP representation: C-terminal amide and Cys2-Cys7 disulfide; N-methylation at Gly24 and Ile26 per the primary source."),
    "0035": structure("KCNTATCATQRLANFLVHSSNNFGPILPPTNVGSNTY", cterm="amide", disulfide_pairs=((1, 6),), note="Mature pramlintide representation: C-terminal amide and Cys2-Cys7 disulfide."),
    "0036": structure("NYGAILSS"),
    "0037": structure("KCNTATCATQRLANFLVHSSNNFGAPLSSTNVGSNTY", cterm="amide", disulfide_pairs=((1, 6),), note="Mature hIAPP representation: C-terminal amide and Cys2-Cys7 disulfide."),
    "0038": structure("KCNTATCATQRLANFLVRSSNNLGPVLPPTNVGSNTY", cterm="amide", disulfide_pairs=((1, 6),), note="Mature rat IAPP representation: C-terminal amide and Cys2-Cys7 disulfide."),
    "0039": structure("KCNTATCATQRLARRRRHSSNNFGAILSSTNVGSNTY", cterm="amide", disulfide_pairs=((1, 6),), note="Mature full-length hIAPP analogue represented with C-terminal amide and Cys2-Cys7 disulfide."),
    "0040": structure("KCNTATCATQRLANFLVHSSNNRRRRLSSTNVGSNTY", cterm="amide", disulfide_pairs=((1, 6),), note="Mature full-length hIAPP analogue represented with C-terminal amide and Cys2-Cys7 disulfide."),
    "0041": structure("KCNTDDDDDHSSNNFGAILSSTNVGSNTY", cterm="amide", note="The truncated sequence retains only one cysteine, so no disulfide bond is encoded; C-terminal amidation follows the mature-IAPP convention."),
    "0042": structure("KCNTATCATQRLANFLVKSSNNFGAILSSTNVGSNTY", cterm="amide", disulfide_pairs=((1, 6),), note="Mature full-length hIAPP analogue represented with C-terminal amide and Cys2-Cys7 disulfide."),
    "0043": structure("KCNTATCATQRLANFLVRSSNNFGAILSSTNVGSNTY", cterm="amide", disulfide_pairs=((1, 6),), note="Mature full-length hIAPP analogue represented with C-terminal amide and Cys2-Cys7 disulfide."),
    "0044": structure("KCNTATCATQRLANFLVESSNNFGAILSSTNVGSNTY", cterm="amide", disulfide_pairs=((1, 6),), note="Mature full-length hIAPP analogue represented with C-terminal amide and Cys2-Cys7 disulfide."),
    "0045": structure("KCNTATCATQRLANFLVASSNNFGAILSSTNVGSNTY", cterm="amide", disulfide_pairs=((1, 6),), note="Mature full-length hIAPP analogue represented with C-terminal amide and Cys2-Cys7 disulfide."),
    "0046": structure("EALYLV"),
    "0047": structure("VEALYLV"),
    "0048": structure("TVYVYSRVK", cterm="amide"),
    "0049": structure("FLPNF"),
    "0050": structure("YY"),
    "0051": structure("YYY"),
    "0052": structure("LTPHKHHKHLHA"),
    "0053": structure("SNNFGAILSS", n_methylated=(4, 6), note="N-methyl groups placed on Gly and Ile as described in the primary study; the source workbook shorthand places markers after the preceding residues."),
    "0054": structure("NFGAIL", n_methylated=(2, 4), note="N-methyl groups placed on Gly and Ile as described in the primary study; the source workbook shorthand places markers after the preceding residues."),
    "0055": structure("RGNFLVHGR", cterm="amide"),
    "0056": structure("RGANFLVHGR", cterm="amide", n_methylated=(2, 4, 6)),
    "0057": structure("RGANFLVHGR", cterm="amide", n_methylated=(3, 5, 7)),
    "0058": structure("KKLTVWIpGKWITVSA", note="D-Pro is encoded at the lowercase p."),
    "0059": structure("KKLWVS IpGK KIWVSA".replace(" ", ""), note="D-Pro is encoded at the lowercase p."),
    "0060": structure("KKLTVYIpGKYITVSA", note="D-Pro is encoded at the lowercase p."),
    "0061": structure("RGNwNeSkMNEYSGWmLmLtMGR", nterm="acetyl", cterm="amide", note="Lowercase residues are encoded as D-amino acids, as specified in the source notation."),
    "0062": structure("BNFBVHSS"),
    "0063": structure("BNFBVH"),
    "0064": structure("BNFBV"),
    "0065": structure("NFGAZL", note="Z is 2-aminobenzoic acid (anthranilic acid), as defined for X2 in the cited source."),
    "0066": structure("NFZAZL", note="Each Z is 2-aminobenzoic acid (anthranilic acid), as defined for X2 in the cited source."),
    "0067": structure("WKKLTVWIpGKWITVSAWTG", nterm="acetyl", cterm="amide", note="Includes the N-terminal Trp present in the primary-paper sequence; the source workbook L-SEQ field omits this residue. D-Pro is encoded at lowercase p."),
    "0068": structure("GKWITVS IpPKKLTVWIp".replace(" ", ""), cyclic_backbone=True, cterm="cyclic", note="Backbone-cyclized as specified by the primary paper; D-Pro is encoded at both lowercase p positions. The source workbook L-SEQ omits one Pro residue."),
    "0069": structure("CFLVHSSNFGAGAILSSC", cterm="amide", disulfide_pairs=((0, 17),), n_methylated=(11, 13), note="Represented as an intramolecular Cys-Cys disulfide macrocycle with C-terminal amide; N-methyl groups placed on Gly and Ile as inferred from the cited MCIP design convention. The source-table sequence counts 18 residues, whereas the article text describes MCIP-2a as a 17-mer; the source-table sequence is retained pending manual reconciliation.", structural_assumption=True),
    "0070": structure("CFGGGGGGGGAGAIGGC", cterm="amide", disulfide_pairs=((0, 16),), n_methylated=(11, 13), note="Represented as an intramolecular Cys-Cys disulfide macrocycle with C-terminal amide; N-methyl groups placed on Gly and Ile as inferred from the cited MCIP design convention.", structural_assumption=True),
    "0071": structure("CfggggggggAGAIGGc", cterm="amide", disulfide_pairs=((0, 16),), n_methylated=(11, 13), note="Lowercase residues are encoded as D-amino acids; represented as an intramolecular Cys-Cys disulfide macrocycle with C-terminal amide. N-methyl groups placed on Gly and Ile as inferred from the cited MCIP design convention.", structural_assumption=True),
    "0072": structure("RRRR", nterm="C14", cterm="amide"),
    "0073": structure("MLRTKDLIWTLFFLGTAVSKKRPKP", cterm="amide"),
    "0074": structure("TNGQ"),
    "0075": structure("MANT"),
    "0076": structure("YMSV"),
}


SIDE_CHAINS = {
    "A": "C", "R": "CCCNC(=N)N", "N": "CC(=O)N", "D": "CC(=O)O",
    "C": "CS", "Q": "CCC(=O)N", "E": "CCC(=O)O", "G": None,
    "H": "CC1=CN=C[NH]1", "I": None, "L": "CC(C)C", "K": "CCCCN",
    "M": "CCSC", "F": "CC1=CC=CC=C1", "P": None, "S": "CO",
    "T": None, "W": "CC1=CNC2=CC=CC=C12", "Y": "CC1=CC=C(O)C=C1",
    "V": "C(C)C",
}

GLYCANS = {
    # D-glucose and N-acetyl-D-glucosamine stereochemistry from PubChem.
    # The anomeric carbon is deliberately left unspecified.
    "Glc": "C([C@@H]1[C@H]([C@@H]([C@H](C(O1)O)O)O)O)O",
    "GlcNAc": "CC(=O)N[C@@H]1[C@H]([C@@H]([C@H](OC1O)CO)O)O",
}


def n_terminal_prefix(spec: dict[str, object], first_token: str) -> str:
    nterm = str(spec["nterm"])
    n_methylated = 0 in spec["n_methylated"]  # type: ignore[operator]
    if spec["cyclic_backbone"]:
        return "N9" + ("(C)" if n_methylated else "")
    if nterm == "free":
        return ("N3" if first_token.upper() == "P" else "N") + ("(C)" if n_methylated else "")
    if nterm == "acetyl":
        return "CC(=O)N3" if first_token.upper() == "P" else "CC(=O)N" + ("(C)" if n_methylated else "")
    if nterm == "C14":
        return "C" * 13 + "C(=O)N" + ("(C)" if n_methylated else "")
    if nterm == "pyromellitate":
        return "O=C(c1c(C(=O)O)cc(C(=O)O)c(C(=O)O)c1)N" + ("3" if first_token.upper() == "P" else "")
    raise ValueError(f"Unsupported N-terminal cap: {nterm}")


def residue_prefix(index: int, token: str, spec: dict[str, object]) -> str:
    if index == 0:
        return n_terminal_prefix(spec, token)
    methylated = index in spec["n_methylated"]  # type: ignore[operator]
    if token.upper() == "P":
        return "N3(C)" if methylated else "N3"
    return "N(C)" if methylated else "N"


def alpha_fragment(index: int, token: str, spec: dict[str, object]) -> str:
    aa = token.upper()
    is_d = token.islower()
    chirality = "@" if is_d else "@@"
    disulfide_indices = {pos for pair in spec["disulfide_pairs"] for pos in pair}  # type: ignore[union-attr]
    glycosylation = spec["glycosylation"]  # type: ignore[assignment]

    if aa == "G":
        return "C"
    if aa == "B":  # Aib, achiral at C-alpha
        return "C(C)(C)"
    if aa == "X":  # alpha,beta-dehydrophenylalanine; E/Z not specified
        return "C(=Cc1ccccc1)"
    if aa == "Z":  # 2-aminobenzoic acid (anthranilic acid)
        return "c1ccccc1"
    if aa == "P":
        return f"[C{chirality}H](CCC3)"
    if aa not in SIDE_CHAINS:
        raise ValueError(f"Unsupported residue token {token!r} at position {index + 1}")

    if aa == "C" and index in disulfide_indices:
        side = "CS8"
    elif aa == "S" and index in glycosylation:
        map_number = 7000 + index
        side = f"C[O:{map_number}]"
    elif aa == "I":
        side = f"[C{'@' if is_d else '@@'}H](C)CC"
    elif aa == "T":
        side = f"[C{'@@' if is_d else '@'}H](O)C"
    else:
        side = SIDE_CHAINS[aa]

    if side is None:
        return f"[C{chirality}H]"
    return f"[C{chirality}H]({side})"


def raw_peptide_smiles(spec: dict[str, object]) -> str:
    tokens = list(str(spec["sequence"]))
    if not tokens:
        raise ValueError("Empty normalized sequence")
    if any(token.upper() not in {*SIDE_CHAINS, "B", "X", "Z"} for token in tokens):
        raise ValueError(f"Unsupported normalized sequence: {spec['sequence']!r}")
    if spec["cyclic_backbone"] and len(tokens) < 2:
        raise ValueError("Backbone cyclization requires at least two residues")

    parts = [n_terminal_prefix(spec, tokens[0])]
    for index, token in enumerate(tokens):
        if index > 0:
            parts.append(residue_prefix(index, token, spec))
        parts.append(alpha_fragment(index, token, spec))
        if index < len(tokens) - 1:
            parts.append("C(=O)")
        elif spec["cyclic_backbone"]:
            parts.append("C(=O)9")
        elif spec["cterm"] == "amide":
            parts.append("C(=O)N")
        elif spec["cterm"] == "acid":
            parts.append("C(=O)O")
        else:
            raise ValueError(f"Unsupported C-terminal state: {spec['cterm']}")
    return "".join(parts)


def attach_glycan(mol: "Chem.Mol", peptide_oxygen_index: int, glycan_name: str) -> "Chem.Mol":
    sugar = Chem.MolFromSmiles(GLYCANS[glycan_name])
    if sugar is None:
        raise ValueError(f"RDKit could not parse {glycan_name} template")
    anomeric = []
    for atom in sugar.GetAtoms():
        if atom.GetAtomicNum() != 6:
            continue
        neighbors = [neighbor.GetAtomicNum() for neighbor in atom.GetNeighbors()]
        if neighbors.count(8) == 2 and neighbors.count(6) == 1:
            anomeric.append(atom.GetIdx())
    if len(anomeric) != 1:
        raise ValueError(f"Could not uniquely identify anomeric carbon in {glycan_name}")
    anomeric_index = anomeric[0]
    free_oxygen = [
        neighbor.GetIdx()
        for neighbor in sugar.GetAtomWithIdx(anomeric_index).GetNeighbors()
        if neighbor.GetAtomicNum() == 8 and neighbor.GetDegree() == 1
    ]
    if len(free_oxygen) != 1:
        raise ValueError(f"Could not identify anomeric hydroxyl oxygen in {glycan_name}")

    offset = mol.GetNumAtoms()
    combined = Chem.CombineMols(mol, sugar)
    editable = Chem.RWMol(combined)
    anomeric_index += offset
    oxygen_index = free_oxygen[0] + offset
    editable.AddBond(peptide_oxygen_index, anomeric_index, Chem.BondType.SINGLE)
    editable.RemoveBond(anomeric_index, oxygen_index)
    editable.RemoveAtom(oxygen_index)
    Chem.SanitizeMol(editable)
    return editable.GetMol()


def build_smiles(spec: dict[str, object]) -> str:
    raw = raw_peptide_smiles(spec)
    mol = Chem.MolFromSmiles(raw)
    if mol is None:
        raise ValueError(f"RDKit rejected generated peptide SMILES: {raw}")

    glyco = spec["glycosylation"]  # type: ignore[assignment]
    for index, glycan_name in glyco.items():
        map_number = 7000 + index
        peptide_oxygen = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetAtomMapNum() == map_number]
        if len(peptide_oxygen) != 1:
            raise ValueError(f"Could not locate glycosylation oxygen at residue {index + 1}")
        mol = attach_glycan(mol, peptide_oxygen[0], str(glycan_name))

    for atom in mol.GetAtoms():
        atom.SetAtomMapNum(0)
    Chem.SanitizeMol(mol)
    return Chem.MolToSmiles(mol, canonical=True, isomericSmiles=True)


def citation_by_entry() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for reference in REFERENCES:
        for entry_id in reference["reference_entry_ids"].split(";"):
            if entry_id in result:
                raise ValueError(f"Duplicate reference-entry mapping: {entry_id}")
            result[entry_id] = reference
    return result


def atomic_write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8-sig", newline="", dir=path.parent, delete=False) as temp:
        temp_path = Path(temp.name)
        writer = csv.DictWriter(
            temp, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temp_path, path)


def run(input_path: Path, output_path: Path, references_path: Path) -> None:
    with input_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        input_fields = list(reader.fieldnames or [])
    if len(rows) != 76:
        raise ValueError(f"Expected 76 hIAPP literature rows; found {len(rows)}")

    citation_lookup = citation_by_entry()
    table_rows: list[dict[str, str]] = []
    for row in rows:
        record_number = row["record_id"].rsplit("-", 1)[-1]
        if record_number not in SPECS:
            raise ValueError(f"Missing structure specification for {row['record_id']}")
        citation = citation_lookup.get(row["reference_entry_id"])
        if citation is None:
            raise ValueError(f"Missing citation mapping for {row['reference_entry_id']}")
        spec = SPECS[record_number]
        smiles = build_smiles(spec)

        notes = []
        if spec["note"]:
            notes.append(str(spec["note"]))
        if not spec["cyclic_backbone"]:
            if spec["nterm_assumed"]:
                notes.append("N-terminal state was not specified; represented as a free amine.")
            if spec["cterm_assumed"]:
                notes.append("C-terminal state was not specified; represented as a carboxylic acid.")
        row["smiles"] = smiles
        has_assumptions = bool(spec["structural_assumption"])
        if not spec["cyclic_backbone"]:
            has_assumptions = has_assumptions or bool(spec["nterm_assumed"] or spec["cterm_assumed"])
        row["smiles_status"] = "computed_with_assumptions" if has_assumptions else "computed_from_explicit_annotations"
        row["smiles_note"] = " ".join(notes)
        row["citation_id"] = citation["reference_id"]
        row["source_citation"] = citation["source_citation"]
        row["citation_status"] = citation["verification_status"]
        if citation["curation_note"]:
            existing = row.get("data_quality_note", "")
            note = f"Citation curation: {citation['curation_note']}"
            if note not in existing:
                row["data_quality_note"] = "; ".join(filter(None, [existing, note]))
        table_rows.append(row)

    fields = [field for field in input_fields if field != "source_smiles"]
    for new_field in ("smiles", "smiles_status", "smiles_note", "citation_id"):
        if new_field not in fields:
            fields.append(new_field)
    reference_fields = [
        "reference_entry_ids", "candidate_names", "source_title", "publication", "year",
        "doi_or_url", "verification_status", "reference_id", "authors", "volume",
        "issue", "pages_or_article", "source_type", "curation_note", "source_citation",
    ]
    atomic_write_csv(output_path, fields, table_rows)
    atomic_write_csv(references_path, reference_fields, REFERENCES)
    print(f"Wrote {len(table_rows)} rows with canonical SMILES using RDKit {rdBase.rdkitVersion}.")
    print(f"Wrote {len(REFERENCES)} normalized hIAPP reference records.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=LITERATURE_CSV)
    parser.add_argument("--output", type=Path, default=LITERATURE_CSV)
    parser.add_argument("--references-output", type=Path, default=REFERENCES_CSV)
    args = parser.parse_args()
    run(args.input, args.output, args.references_output)


if __name__ == "__main__":
    main()
