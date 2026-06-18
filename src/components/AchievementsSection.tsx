import { useState } from 'react';
import SectionBlock from './SectionBlock';
import {
  Dialog,
  DialogContent,
  DialogTrigger,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog';
import { ArrowUpRight, Award } from 'lucide-react';

type Category = 'All' | 'Hackathon' | 'Bootcamp' | 'Workshop' | 'Internship';

const achievements: {
  title: string;
  issuer: string;
  date: string;
  description: string;
  image: string;
  category: Exclude<Category, 'All'>;
}[] = [
  {
    title: 'Site of the Day',
    issuer: 'Awwwards',
    date: 'March 2025',
    description: 'Awarded for outstanding creative and technical achievement on Project Nebula.',
    image: 'https://images.unsplash.com/photo-1579546929518-9e396f3cc809?q=80&w=2670&auto=format&fit=crop',
    category: 'Hackathon', // using existing category enum
  },
  {
    title: 'FWA of the Month',
    issuer: 'The FWA',
    date: 'January 2025',
    description: 'Recognized for pushing the boundaries of immersive web experiences.',
    image: 'https://images.unsplash.com/photo-1557672172-298e090bd0f1?q=80&w=2574&auto=format&fit=crop',
    category: 'Internship',
  },
];

const CATEGORIES: Category[] = [
  'All',
  'Hackathon',
  'Bootcamp',
  'Workshop',
  'Internship',
];

const categoryAccent: Record<Exclude<Category, 'All'>, string> = {
  Hackathon: 'bg-black text-white',
  Bootcamp: 'bg-black text-white',
  Workshop: 'bg-black text-white',
  Internship: 'bg-black text-white',
};

const categoryBorder: Record<Exclude<Category, 'All'>, string> = {
  Hackathon: 'border-black',
  Bootcamp: 'border-black',
  Workshop: 'border-black',
  Internship: 'border-black',
};

const AchievementsSection = () => {
  const [active, setActive] = useState<Category>('All');
  const [hovered, setHovered] = useState<number | null>(null);

  const filtered =
    active === 'All'
      ? achievements
      : achievements.filter((a) => a.category === active);

  return (
    <SectionBlock id="achievements" title="Achievements">
      {/* ── Top bar ──────────────────────────────────────────────── */}
      <div className="mb-8 pb-6 border-b-2 border-black/10 space-y-4">
        {/* Stats row */}
        <div className="flex items-center gap-3">
          <Award className="w-4 h-4 shrink-0" />
          <span className="font-mono text-xs sm:text-sm font-bold tracking-widest uppercase">
            {achievements.length} Certificates
          </span>
          <span className="font-mono text-xs text-foreground/40">
            / {filtered.length} shown
          </span>
        </div>

        {/* Filter pills — horizontally scrollable on mobile */}
        <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-none">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setActive(cat)}
              className={`font-mono text-[10px] sm:text-[11px] tracking-widest uppercase px-3 sm:px-4 py-1.5 border-2 transition-all duration-200 whitespace-nowrap shrink-0 ${
                active === cat
                  ? 'bg-black text-white border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,0.25)]'
                  : 'bg-transparent text-foreground border-black/25 hover:border-black hover:shadow-[3px_3px_0px_0px_rgba(0,0,0,1)]'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* ── Awwwards List ─────────────────────────────────────────── */}
      <div className="border-t-2 border-black">
        {filtered.map((item, idx) => (
          <Dialog key={item.title}>
            <DialogTrigger asChild>
              {/* ── Row wrapper */}
              <div
                role="button"
                tabIndex={0}
                aria-label={`View certificate: ${item.title}`}
                className="group relative border-b-2 border-black cursor-pointer overflow-hidden focus:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-offset-2"
                onMouseEnter={() => setHovered(idx)}
                onMouseLeave={() => setHovered(null)}
              >
                {/* ── Black fill slides up on hover (desktop only) */}
                <div
                  className="absolute inset-0 bg-black translate-y-full group-hover:translate-y-0 transition-transform duration-[480ms] ease-[cubic-bezier(0.76,0,0.24,1)] pointer-events-none hidden sm:block"
                  aria-hidden="true"
                />

                {/* ── Thumbnail slides in from right on desktop hover */}
                <div
                  className="absolute top-0 right-0 h-full w-44 lg:w-56 z-10 overflow-hidden pointer-events-none
                              translate-x-full group-hover:translate-x-0
                              transition-transform duration-[480ms] ease-[cubic-bezier(0.76,0,0.24,1)]
                              hidden sm:block"
                  aria-hidden="true"
                >
                  <img
                    src={item.image}
                    alt=""
                    className="w-full h-full object-cover object-top"
                  />
                  <div className="absolute inset-0 bg-black/50" />
                  <div
                    className={`absolute left-0 top-0 h-full border-l-4 ${categoryBorder[item.category]}`}
                  />
                </div>

                {/* ═══════════════════════════════════
                    MOBILE layout  (< sm)
                    Small thumbnail always visible + stacked text
                ════════════════════════════════════ */}
                <div className="flex sm:hidden items-start gap-3 px-4 py-4 active:bg-black/5 transition-colors">
                  {/* Thumbnail */}
                  <div className="w-16 h-16 shrink-0 overflow-hidden border-2 border-black/20">
                    <img
                      src={item.image}
                      alt={item.title}
                      className="w-full h-full object-cover object-top"
                    />
                  </div>

                  {/* Text block */}
                  <div className="flex-1 min-w-0">
                    {/* Category + date on same line */}
                    <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                      <span
                        className={`text-[9px] font-mono font-black px-1.5 py-0.5 leading-none ${categoryAccent[item.category]}`}
                      >
                        {item.category.toUpperCase()}
                      </span>
                      <span className="font-mono text-[9px] text-foreground/40 tracking-widest uppercase">
                        {item.date}
                      </span>
                    </div>
                    <h3 className="font-black text-sm leading-snug tracking-tight mb-0.5 line-clamp-2">
                      {item.title}
                    </h3>
                    <p className="font-mono text-[10px] text-foreground/50 line-clamp-1">
                      {item.issuer}
                    </p>
                  </div>

                  {/* Arrow */}
                  <ArrowUpRight className="w-4 h-4 text-foreground/25 mt-1 shrink-0" />
                </div>

                {/* ═══════════════════════════════════
                    TABLET / DESKTOP layout  (≥ sm)
                    Full awwwards row
                ════════════════════════════════════ */}
                <div className="hidden sm:flex items-center gap-4 lg:gap-6 px-6 lg:px-8 py-5 lg:py-6 pr-[12rem] lg:pr-[15rem] relative z-20 transition-colors duration-[480ms]">
                  {/* Index */}
                  <span className="font-mono text-xs font-bold text-foreground/25 group-hover:text-white/30 transition-colors duration-300 w-6 shrink-0 select-none">
                    {String(idx + 1).padStart(2, '0')}
                  </span>

                  {/* Category pill */}
                  <span
                    className={`text-[10px] font-mono font-black px-2 py-1 shrink-0 leading-none ${categoryAccent[item.category]}`}
                  >
                    {item.category.toUpperCase()}
                  </span>

                  {/* Title + issuer */}
                  <div className="flex-1 min-w-0">
                    <h3 className="font-black text-base lg:text-lg leading-tight tracking-tight group-hover:text-white transition-colors duration-300 line-clamp-1">
                      {item.title}
                    </h3>
                    <p className="font-mono text-xs text-foreground/50 group-hover:text-white/50 transition-colors duration-300 mt-0.5">
                      {item.issuer}
                    </p>
                  </div>

                  {/* Tag chip — desktop only */}
                  <span className="hidden lg:inline-block font-mono text-[10px] border border-black/20 group-hover:border-white/30 px-2 py-1 text-foreground/50 group-hover:text-white/50 transition-colors duration-300 shrink-0">
                    {item.tag}
                  </span>

                  {/* Date */}
                  <span className="font-mono text-[10px] tracking-widest uppercase text-foreground/35 group-hover:text-white/40 transition-colors duration-300 shrink-0">
                    {item.date}
                  </span>

                  {/* Arrow */}
                  <ArrowUpRight className="w-5 h-5 text-foreground/25 group-hover:text-white group-hover:rotate-12 transition-all duration-300 shrink-0" />
                </div>
              </div>
            </DialogTrigger>

            {/* ── Lightbox ─────────────────────────────────────────── */}
            <DialogContent
              className="
                w-[95vw] max-w-5xl p-0
                border-2 sm:border-4 border-black
                rounded-none
                shadow-[8px_8px_0px_0px_rgba(0,0,0,0.6)] sm:shadow-[20px_20px_0px_0px_rgba(0,0,0,0.85)]
                overflow-hidden bg-white
                max-h-[90vh] overflow-y-auto
              "
            >
              <DialogTitle className="sr-only">{item.title}</DialogTitle>
              <DialogDescription className="sr-only">
                {item.issuer} — {item.category}
              </DialogDescription>

              {/* Stacks vertically on mobile, side-by-side on md+ */}
              <div className="flex flex-col md:flex-row h-full">
                {/* Image panel */}
                <div className="flex-1 bg-black/5 flex items-center justify-center p-3 sm:p-4 min-h-[200px] sm:min-h-[45vh]">
                  <img
                    src={item.image}
                    alt={item.title}
                    className="w-full h-auto max-h-[50vh] sm:max-h-[72vh] object-contain"
                  />
                </div>

                {/* Details sidebar */}
                <div className="md:w-72 p-4 sm:p-6 border-t-2 md:border-t-0 md:border-l-4 border-black flex flex-col justify-between bg-white">
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <span
                        className={`text-[10px] font-mono font-black px-2 py-1 ${categoryAccent[item.category]}`}
                      >
                        {item.category.toUpperCase()}
                      </span>
                      <span className="font-mono text-xs text-foreground/30 font-bold">
                        {String(filtered.indexOf(item) + 1).padStart(2, '0')}
                      </span>
                    </div>

                    <h2 className="font-black text-lg sm:text-xl leading-tight mb-2 tracking-tight">
                      {item.title}
                    </h2>
                    <p className="font-mono text-sm text-foreground/70 font-semibold mb-1">
                      {item.issuer}
                    </p>
                    <p className="font-mono text-xs text-foreground/35 tracking-widest uppercase mb-4 sm:mb-6">
                      {item.date}
                    </p>
                    <p className="text-sm text-foreground/65 leading-relaxed">
                      {item.description}
                    </p>
                  </div>

                  <div className="mt-4 sm:mt-6 pt-4 border-t-2 border-black/10 flex items-center justify-between">
                    <span className="font-mono text-xs bg-black text-white px-3 py-1.5 inline-block font-bold tracking-wider">
                      {item.tag}
                    </span>
                    <span className="font-mono text-[10px] text-foreground/30 uppercase tracking-widest">
                      Certificate
                    </span>
                  </div>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        ))}
      </div>

      {/* ── Empty state */}
      {filtered.length === 0 && (
        <div className="flex flex-col items-center justify-center py-16 sm:py-24 border-b-2 border-black text-foreground/30">
          <Award className="w-10 h-10 mb-3 opacity-20" />
          <p className="font-mono text-sm">No certificates in this category</p>
        </div>
      )}
    </SectionBlock>
  );
};

export default AchievementsSection;
