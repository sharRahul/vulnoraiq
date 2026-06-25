import { useEffect, useState } from "react";
import {
  AlertTriangle,
  CheckCircle2,
  FileCode,
  FolderOpen,
  Loader2,
  Package,
  RefreshCw,
  Rocket,
  Search,
  Server,
  Terminal,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface EnvVar {
  name: string;
  required: boolean;
  suggested: string;
}

interface Endpoint {
  method: string;
  path: string;
  param_style: string;
  param_key?: string;
}

interface Project {
  name: string;
  exists: boolean;
  framework: string | null;
  ports: number[];
  endpoints: Endpoint[];
  env_vars: EnvVar[];
  has_dockerfile: boolean;
  has_requirements: boolean;
  has_pyproject: boolean;
  readme: string;
  file_count: number;
  errors: string[];
}

async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(path, { credentials: "same-origin", ...options });
  if (!response.ok) throw new Error(await response.text());
  return response.json() as Promise<T>;
}

async function csrfToken(): Promise<string> {
  return (await api<{ csrf_token: string }>("/api/csrf-token")).csrf_token;
}

export function ProjectImporter() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selected, setSelected] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deploying, setDeploying] = useState(false);
  const [envValues, setEnvValues] = useState<Record<string, string>>({});
  const [search, setSearch] = useState("");

  async function loadProjects() {
    setLoading(true);
    setError(null);
    try {
      const data = await api<{ projects: Project[] }>("/api/projects");
      setProjects(data.projects || []);
    } catch (exc) {
      setError(exc instanceof Error ? exc.message : String(exc));
    } finally {
      setLoading(false);
    }
  }

  async function selectProject(name: string) {
    setError(null);
    try {
      const data = await api<Project>(`/api/projects/${encodeURIComponent(name)}/analyze`);
      setSelected(data);
      const defaults: Record<string, string> = {};
      data.env_vars?.forEach((v) => { defaults[v.name] = v.suggested || ""; });
      setEnvValues(defaults);
    } catch (exc) {
      setError(exc instanceof Error ? exc.message : String(exc));
    }
  }

  async function deployProject(projectName: string) {
    setDeploying(true);
    setError(null);
    try {
      const token = await csrfToken();
      const filled: Record<string, string> = {};
      Object.entries(envValues).forEach(([k, v]) => { if (v.trim()) filled[k] = v.trim(); });
      await api("/api/projects/deploy", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRF-Token": token },
        body: JSON.stringify({ project: projectName, env: filled }),
      });
      await loadProjects();
    } catch (exc) {
      setError(exc instanceof Error ? exc.message : String(exc));
    } finally {
      setDeploying(false);
    }
  }

  useEffect(() => { void loadProjects(); }, []);

  const filtered = projects.filter((p) => !search || p.name.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="h-full overflow-y-auto p-4 scrollbar-thin sm:p-6">
      <div className="mx-auto max-w-[1400px] space-y-4">
        <div className="rounded-xl border border-border bg-card p-4 shadow-card">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div className="min-w-0">
              <p className="text-xs font-bold uppercase tracking-wide text-muted-foreground">Project Importer</p>
              <h1 className="ui-title-row mt-1 text-2xl font-extrabold">
                <FolderOpen className="size-6" /> <span>Import & Deploy AI Projects</span>
              </h1>
              <p className="mt-1 max-w-3xl text-sm text-muted-foreground">
                Place your AI app source code in <code className="rounded bg-muted px-1">./projects/</code> on the host. VulnoraIQ will analyze it, build a Docker image, and auto-register scan targets.
              </p>
            </div>
            <Button variant="secondary" onClick={() => void loadProjects()}><RefreshCw /> <span>Refresh</span></Button>
          </div>
          {error ? <div className="mt-4 rounded-lg border border-[var(--sev-high)] bg-[var(--sev-high)]/10 p-3 text-sm"><p className="ui-title-row font-bold"><AlertTriangle className="size-4 shrink-0" /> <span>{error}</span></p></div> : null}
        </div>

        <div className="grid gap-4 lg:grid-cols-[minmax(280px,360px)_minmax(0,1fr)]">
          <aside className="space-y-3">
            <div className="relative">
              <Search className="pointer-events-none absolute left-2 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
              <input value={search} onChange={(e) => setSearch(e.target.value)} className="input pl-8 text-sm" placeholder="Filter projects…" />
            </div>
            {loading ? <p className="text-sm text-muted-foreground">Scanning projects…</p> : null}
            <div className="space-y-2">
              {filtered.map((proj) => (
                <button key={proj.name} onClick={() => void selectProject(proj.name)} className={cn("w-full rounded-lg border p-3 text-left transition-colors", selected?.name === proj.name ? "border-primary bg-muted" : "border-border bg-card hover:bg-muted")}>
                  <div className="flex items-start justify-between gap-2">
                    <span className="font-semibold text-sm">{proj.name}</span>
                    <span className="shrink-0 rounded bg-muted px-2 py-0.5 text-[10px] font-bold uppercase text-muted-foreground">{proj.framework || "unknown"}</span>
                  </div>
                  <p className="mt-1 text-xs text-muted-foreground">{proj.file_count} files · {proj.ports?.join(", ") || "no ports detected"} · {proj.endpoints?.length || 0} endpoints</p>
                  <div className="mt-1.5 flex flex-wrap gap-1">
                    {proj.has_dockerfile ? <span className="inline-flex items-center gap-0.5 rounded bg-[var(--accent-sage)]/20 px-1.5 py-0.5 text-[10px] font-semibold text-[var(--accent-sage)]"><CheckCircle2 className="size-3" /> Dockerfile</span> : null}
                    {proj.has_requirements ? <span className="inline-flex items-center gap-0.5 rounded bg-muted px-1.5 py-0.5 text-[10px] font-semibold text-muted-foreground">requirements.txt</span> : null}
                  </div>
                </button>
              ))}
              {!loading && filtered.length === 0 ? <p className="rounded-lg border border-border bg-card p-4 text-sm text-muted-foreground text-center">No projects found. Add folders to <code className="rounded bg-muted px-1">./projects/</code> on the host.</p> : null}
            </div>
          </aside>

          <section className="space-y-4">
            {!selected ? (
              <div className="rounded-xl border border-border bg-card p-8 text-center shadow-card">
                <FolderOpen className="mx-auto mb-3 size-12 text-muted-foreground/30" />
                <p className="text-sm text-muted-foreground">Select a project from the left to inspect and deploy it.</p>
              </div>
            ) : (
              <>
                <div className="rounded-xl border border-border bg-card p-4 shadow-card">
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div className="min-w-0">
                      <h2 className="ui-title-row text-xl font-extrabold"><FileCode className="size-5" /> <span>{selected.name}</span></h2>
                      <p className="text-xs text-muted-foreground mt-0.5">{selected.framework || "Unknown framework"} · {selected.file_count} Python files · {selected.ports?.length || 0} ports</p>
                    </div>
                    <Button variant="success" disabled={deploying} onClick={() => void deployProject(selected.name)}>
                      {deploying ? <Loader2 className="size-4 animate-spin" /> : <Rocket className="size-4" />}
                      <span>Build & Deploy</span>
                    </Button>
                  </div>
                </div>

                {selected.env_vars?.length ? (
                  <div className="rounded-xl border border-border bg-card p-4 shadow-card">
                    <h3 className="ui-title-row font-bold"><Terminal className="size-4" /> <span>Environment Variables</span></h3>
                    <p className="text-xs text-muted-foreground mt-1">Set values required by the project. Required vars are marked.</p>
                    <div className="mt-3 space-y-2">
                      {selected.env_vars.map((v) => (
                        <label key={v.name} className="block">
                          <span className="text-xs font-semibold">
                            {v.name}
                            {v.required ? <span className="ml-1 text-[var(--sev-high)]">*required</span> : null}
                          </span>
                          <input value={envValues[v.name] || ""} onChange={(e) => setEnvValues((prev) => ({ ...prev, [v.name]: e.target.value }))} className="input mt-0.5 font-mono text-sm" placeholder={v.required ? `Enter ${v.name}…` : "(optional)"} />
                        </label>
                      ))}
                    </div>
                  </div>
                ) : null}

                {selected.endpoints?.length ? (
                  <div className="rounded-xl border border-border bg-card p-4 shadow-card">
                    <h3 className="ui-title-row font-bold"><Server className="size-4" /> <span>Detected Endpoints</span></h3>
                    <p className="text-xs text-muted-foreground mt-1">These will be auto-registered as scan targets after deploy.</p>
                    <div className="mt-3 space-y-2">
                      {selected.endpoints.map((ep, i) => (
                        <div key={i} className="rounded-lg border border-border bg-canvas p-3">
                          <div className="flex items-center gap-2">
                            <span className={cn("rounded px-1.5 py-0.5 text-[10px] font-bold uppercase", ep.method === "GET" ? "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200" : "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200")}>{ep.method}</span>
                            <code className="font-mono text-sm">{ep.path}</code>
                          </div>
                          <p className="mt-1 text-xs text-muted-foreground">Param style: {ep.param_style}{ep.param_key ? ` · key: "${ep.param_key}"` : ""}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : null}

                {selected.readme ? (
                  <div className="rounded-xl border border-border bg-card p-4 shadow-card">
                    <h3 className="ui-title-row font-bold"><Package className="size-4" /> <span>README</span></h3>
                    <pre className="mt-2 max-h-48 overflow-auto whitespace-pre-wrap rounded-lg bg-muted p-3 text-xs text-muted-foreground font-sans scrollbar-thin">{selected.readme}</pre>
                  </div>
                ) : null}
              </>
            )}
          </section>
        </div>
      </div>
    </div>
  );
}
