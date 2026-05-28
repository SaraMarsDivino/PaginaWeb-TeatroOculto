import { defineCollection, z } from 'astro:content';

const obras = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    synopsis: z.string(),
    poster: z.string(),
    release_date: z.string().optional(),
    active: z.boolean().default(true),
    gallery: z.array(z.string()).default([]),
    duration: z.string().optional(),
    cast: z.array(z.string()).default([]),
  }),
});

const iniciativas = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    category: z.enum(['Creación', 'Formación', 'Comunidad']),
    image: z.string(),
    order: z.number().default(0),
  }),
});

export const collections = { obras, iniciativas };
