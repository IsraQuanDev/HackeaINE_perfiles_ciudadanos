import { NextRequest, NextResponse } from "next/server";
import { execFile } from "child_process";
import path from "path";

export async function POST(req: NextRequest): Promise<NextResponse> {
  try {
    const body = await req.json();
    const question = String(body?.question ?? "").trim();
    if (!question) {
      return NextResponse.json({ error: "Pregunta vacía" }, { status: 400 });
    }

    const repoRoot = path.resolve(process.cwd(), "..");
    const pyScript = `
import json, sys
from src.llm.text_to_sql import answer_data_question
q = sys.argv[1]
res = answer_data_question(q)
print(json.dumps(res.model_dump(), ensure_ascii=False))
`;

    const resultJson = await new Promise<string>((resolve, reject) => {
      execFile(
        "python",
        ["-c", pyScript, question],
        { cwd: repoRoot, timeout: 8000, env: { ...process.env, PYTHONIOENCODING: "utf-8" } },
        (err, stdout, stderr) => {
          if (err) {
            reject(new Error(stderr || err.message));
            return;
          }
          resolve(stdout.trim());
        }
      );
    });

    return NextResponse.json(JSON.parse(resultJson));
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : "Error interno";
    return NextResponse.json({ error: msg }, { status: 500 });
  }
}
