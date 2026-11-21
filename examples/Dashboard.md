---
cssclasses:
  - dashboard-v4
---
> [!abstract] SmartKnowledge
> [[System/Bases/Projects.base|Projects]] [[System/Bases/Notes.base|Notes]] [[System/Bases/Resources.base|Resources]] [[System/VAULT_RULES|Quy tắc Vault]]
>
> ```dataviewjs
> const row = dv.el("div", "", { cls: "sk-dash-actions" });
> const makeBtn = (svg, label, cls, onClick) => {
>   const b = row.createEl("button", { cls: `sk-dash-btn ${cls || ""}`.trim() });
>   b.innerHTML = `${svg}<span>${label}</span>`;
>   b.onclick = onClick;
>   return b;
> };
>
> const icons = {
>   daily: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>`,
>   search: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>`,
>   task: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>`,
>   note: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M12 18v-6M9 15h6"/></svg>`,
>   imp: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>`,
>   box: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12"/></svg>`,
>   graph: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="7" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="M8.1 7.3 15.6 7M7.3 8.2l3.4 7.6M16.6 9.1l-3.3 6.7"/></svg>`
> };
>
> makeBtn(icons.daily, "Daily Note", "sk-dash-btn-primary", () => app.commands.executeCommandById("daily-notes"));
> makeBtn(icons.search, "Tìm nhanh", "", () => app.commands.executeCommandById("omnisearch:show-modal"));
> makeBtn(icons.task, "Thêm Task", "", () => {
>   if (!app.commands.executeCommandById("obsidian-tasks-plugin:edit-task")) {
>     app.commands.executeCommandById("daily-notes");
>   }
> });
> makeBtn(icons.note, "Note mới", "", () => app.commands.executeCommandById("file-explorer:new-file"));
> makeBtn(icons.imp, "Import", "", () => {
>   const input = document.createElement("input");
>   input.type = "file";
>   input.multiple = true;
>   input.onchange = async () => {
>     const files = Array.from(input.files || []);
>     if (!files.length) return;
>     const ensureDir = async (dir) => {
>       if (!(await app.vault.adapter.exists(dir))) await app.vault.createFolder(dir);
>     };
>     const saved = [];
>     for (const f of files) {
>       const name = f.name;
>       const lower = name.toLowerCase();
>       const ext = lower.includes(".") ? lower.slice(lower.lastIndexOf(".")) : "";
>       let dir = "Inbox/Capture";
>       if (lower.includes("jpd") || lower.includes("fall26")) dir = "Projects/JPD";
>       else if ([".pdf", ".epub", ".mobi", ".azw3"].includes(ext)) dir = "Resources/Books";
>       else if ([".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"].includes(ext)) dir = "System/Attachments";
>       await ensureDir(dir);
>       let target = `${dir}/${name}`;
>       if (await app.vault.adapter.exists(target)) {
>         const dot = name.lastIndexOf(".");
>         const stamp = Date.now().toString().slice(-5);
>         target = dot > 0 ? `${dir}/${name.slice(0, dot)}_${stamp}${name.slice(dot)}` : `${dir}/${name}_${stamp}`;
>       }
>       const buf = await f.arrayBuffer();
>       await app.vault.createBinary(target, buf);
>       saved.push(target);
>     }
>     new Notice(`Đã import ${saved.length} file:\n${saved.join("\n")}`, 6000);
>   };
>   input.click();
> });
> makeBtn(icons.box, "Importer", "", () => app.commands.executeCommandById("obsidian-importer:open-modal"));
> makeBtn(icons.graph, "Graph", "", () => {
>   app.workspace.rightSplit?.expand();
>   if (!app.commands.executeCommandById("graph:open-local")) {
>     app.commands.executeCommandById("graph:open");
>   }
> });
> ```

> [!multi-column]
>
> > [!calendar] Lịch & Tiến độ tuần (Calendar)
> > ![[System/Bases/Projects.base#Calendar]]
>
> > [!todo] Việc cần làm gấp (Urgent Tasks)
> > ```tasks
> > not done
> > description regex matches /\S/
> > path does not include Templates
> > path does not include System
> > path does not include Archive
> > path does not include research
> > path does not include smart_home_project
> > short mode
> > sort by due
> > limit 8
> > ```

> [!multi-column]
>
> > [!example] Bảng Kanban Dự án (Projects)
> > ![[System/Bases/Projects.base#KanbanProjects]]
>
> > [!tip] Truy cập nhanh (Quick Notes)
> > <div class="sk-sticky-grid">
> >   <div class="sk-sticky sk-sticky-yellow">
> >     <div>
> >       <div class="sk-sticky-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>Inbox</div>
> >       <span>Thu thập nhanh</span>
> >     </div>
> >     <a data-href="Inbox" class="internal-link">Mở →</a>
> >   </div>
> >   <div class="sk-sticky sk-sticky-peach">
> >     <div>
> >       <div class="sk-sticky-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/></svg>Projects</div>
> >       <span>Cards & Table</span>
> >     </div>
> >     <a data-href="System/Bases/Projects.base" class="internal-link">Mở →</a>
> >   </div>
> >   <div class="sk-sticky sk-sticky-mint">
> >     <div>
> >       <div class="sk-sticky-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>Areas</div>
> >       <span>Thói quen & mục tiêu</span>
> >     </div>
> >     <a data-href="Areas" class="internal-link">Mở →</a>
> >   </div>
> >   <div class="sk-sticky sk-sticky-coral">
> >     <div>
> >       <div class="sk-sticky-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>Notes</div>
> >       <span>Kho MOC & ghi chú</span>
> >     </div>
> >     <a data-href="Notes/Notes" class="internal-link">Mở →</a>
> >   </div>
> >   <div class="sk-sticky sk-sticky-sky">
> >     <div>
> >       <div class="sk-sticky-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>Resources</div>
> >       <span>Tài liệu & sách</span>
> >     </div>
> >     <a data-href="System/Bases/Resources.base" class="internal-link">Mở →</a>
> >   </div>
> >   <div class="sk-sticky sk-sticky-lilac">
> >     <div>
> >       <div class="sk-sticky-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>Rules</div>
> >       <span>Quy tắc Vault</span>
> >     </div>
> >     <a data-href="System/VAULT_RULES" class="internal-link">Mở →</a>
> >   </div>
> > </div>
