interface CrudPageProps {
  resource: string;
  title: string;
}

export default function CrudPage({ title }: CrudPageProps) {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-slate-800 mb-4">{title}</h1>
      <div className="bg-white rounded-xl border border-slate-200 p-8 text-center text-slate-400">
        CRUD table for {title} will be built here.
      </div>
    </div>
  );
}
