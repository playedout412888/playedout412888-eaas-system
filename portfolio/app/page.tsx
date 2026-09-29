import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "James Fitzgerald — Developer & AI Systems Engineer",
  description: "Developer portfolio and engineering record for James Fitzgerald and 21amG.",
};

const projects = [
  ["Nexus", "RECOVERED / IN BUILD", "The 21amG control architecture for agents, skills, events, execution, memory, policy, and verification.", ["AI orchestration", "Agents", "MCP", "Event-driven"]],
  ["Runable Core", "RECOVERED / IN BUILD", "A voice-first activation fabric connecting Siri and Shortcuts to typed intents, policy gates, agent actions, and spoken results.", ["Siri", "Shortcuts", "Webhooks", "Automation"]],
  ["EaaS Control Plane", "VERIFIED", "A GitHub-centered control plane for structured jobs, specialist workflows, CI validation, provenance, and controlled deployment.", ["GitHub", "CI/CD", "Control plane", "Provenance"]],
  ["James Towing", "RECOVERED / VERIFICATION PENDING", "A production-oriented towing and recovery platform concept for Metro Detroit, including dispatch, customer workflows, local SEO, and operations.", ["Next.js", "Operations", "Dispatch", "SEO"]],
] as const;

const stack = ["Next.js", "TypeScript", "Python", "FastAPI", "PostgreSQL", "Supabase", "Neon", "Vercel", "GitHub Actions", "MCP", "REST APIs", "Apple Shortcuts"];

export default function Home() {
  return <main>
    <nav className="nav"><a className="brand" href="#top">21amG<span>.</span></a><div className="navLinks"><a href="#systems">Systems</a><a href="#architecture">Architecture</a><a href="#stack">Stack</a><a href="#contact">Contact</a></div></nav>
    <section className="hero" id="top"><div className="eyebrow">21amG / ENGINEERING RECORD</div><h1>James Fitzgerald</h1><p className="lead">Developer, systems builder, and AI automation architect building software that can observe, reason, execute, verify, and improve.</p><div className="actions"><a className="button primary" href="#systems">Explore the systems</a><a className="button" href="https://github.com/playedout412888">View GitHub</a></div><div className="heroGrid"><div><b>01</b><span>Autonomous agents</span></div><div><b>02</b><span>Voice-first automation</span></div><div><b>03</b><span>Production control planes</span></div></div></section>
    <section className="section" id="architecture"><div className="sectionHead"><div className="eyebrow">THE CORE MODEL</div><h2>One platform. Many capabilities.</h2><p>21amG is the parent engineering identity. Nexus is the brain and operational controller. Applications remain independently deployable while sharing contracts, provenance, and orchestration.</p></div><div className="flow">{["OBSERVE","UNDERSTAND","CLASSIFY","PLAN","AUTHORIZE","EXECUTE","VERIFY","RECORD","LEARN"].map((x,i)=><div className="flowItem" key={x}><span>{String(i+1).padStart(2,"0")}</span>{x}</div>)}</div></section>
    <section className="section" id="systems"><div className="sectionHead"><div className="eyebrow">SELECTED SYSTEMS</div><h2>Proof of work, not just a résumé.</h2><p>Projects are presented with explicit provenance states rather than treating an idea as an implemented product.</p></div><div className="cards">{projects.map(([name,status,description,tags])=><article className="card" key={name}><div className="cardTop"><span>{status}</span><span>21amG</span></div><h3>{name}</h3><p>{description}</p><div className="tags">{tags.map(tag=><span key={tag}>{tag}</span>)}</div></article>)}</div></section>
    <section className="section split" id="stack"><div><div className="eyebrow">ENGINEERING STACK</div><h2>The tools behind the systems.</h2></div><div className="stack">{stack.map(item=><span key={item}>{item}</span>)}</div></section>
    <section className="terminal"><div className="terminalBar"><i>●</i><i>●</i><i>●</i><b>NEXUS / EXECUTION</b></div><pre>{`21amG@nexus:~$ system status
IDENTITY       21amG
CONTROLLER     NEXUS
MODE           EVENT-DRIVEN
AUTHORIZATION  POLICY-GATED
EXECUTION      VERIFIED-BY-DEFAULT

> observe event
> classify capability
> plan execution graph
> authorize action
> execute through provider
> validate result
> record provenance

STATUS         READY`}</pre></section>
    <footer id="contact"><div><div className="eyebrow">BUILD WITH ME</div><h2>Have a system worth building?</h2><p>Architecture, automation, AI-native applications, and production engineering.</p></div><a className="button primary" href="https://github.com/playedout412888">GitHub / Contact</a></footer>
  </main>;
}