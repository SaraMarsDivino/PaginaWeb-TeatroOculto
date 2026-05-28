export interface TeamMember {
  name: string;
  role: string;
  photo: string;
  bio: string;
  bioExtended?: string;
  credentials: string[];
}

export const equipo: TeamMember[] = [
  {
    name: 'Pablo Valencia Fernández',
    role: 'Director Ejecutivo',
    photo: '/images/nosotros/pablo-valencia.jpg',
    credentials: ['Lic. Artes Escénicas — UPLA', 'Diplomado en Pedagogía Teatral', 'Magíster en Artes — PUC'],
    bio: 'Actor y gestor cultural. Su labor articula la creación artística con la gestión cultural y los procesos formativos.',
    bioExtended:
      'Se desempeña como Director Ejecutivo de Teatro Oculto. Su labor articula la creación artística con la gestión cultural y los procesos formativos, abarcando áreas como producción escénica, dirección, dramaturgia, docencia y canto lírico, con un fuerte énfasis en la vinculación territorial y comunitaria.',
  },
  {
    name: 'Estefania Villalobos',
    role: 'Equipo Ejecutivo',
    photo: '/images/nosotros/estefania-villalobos.jpg',
    credentials: ['Actriz — Especialidad Pedagogía Teatral, UV', 'Locutora certificada — PROVOZ'],
    bio: 'Actriz, locutora y doblajista. Coordinadora de los Talleres Municipales de Teatro de la I. Municipalidad de Quillota.',
    bioExtended:
      'Su trayectoria integra el trabajo en actuación para teatro, cine y televisión, así como en dramaturgia y locución, desarrollando proyectos de narración para audiolibros, e-learning y publicidad. Actualmente se desempeña como coordinadora y docente de los Talleres Municipales de Teatro.',
  },
  {
    name: 'Fabián Zúñiga',
    role: 'Equipo Ejecutivo',
    photo: '/images/nosotros/fabian-zuniga.jpg',
    credentials: ['Lic. Actuación — Dirección, PUC', 'Diplomado en Pedagogía Teatral — PUC'],
    bio: 'Artista escénico con experiencia en actuación teatral, proyectos audiovisuales y formación como tallerista.',
    bioExtended:
      'Cuenta con experiencia en actuación teatral, proyectos audiovisuales y en el ámbito de la formación como tallerista teatral. Es integrante del equipo ejecutivo de Teatro Oculto, aportando desde la creación escénica y los procesos pedagógicos.',
  },
  {
    name: 'Camila Estay Ancieta',
    role: 'Equipo Ejecutivo',
    photo: '/images/nosotros/camila-emilce.jpg',
    credentials: ['Lic. Teatro — mención Didáctica Teatral, UV'],
    bio: 'Actriz con experiencia en actuación teatral, audiovisual y diseño teatral.',
    bioExtended:
      'Cuenta con experiencia en actuación teatral y audiovisual, así como en el ámbito del diseño teatral, integrando la creación escénica con procesos pedagógicos. Es integrante del equipo ejecutivo de Teatro Oculto.',
  },
];
