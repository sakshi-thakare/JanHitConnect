import { NextResponse } from "next/server";
import { query } from "@/app/lib/db";

async function getSummary(complaint2) {
  const responce = await fetch("http://127.0.0.1:5000/summarize", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ complaint: complaint2 }),
  });
  const data = await responce.json();
  // console.log(data);
  return data.summary;
}
async function getMinistry(title, description) {
  const responce = await fetch("http://127.0.0.1:5000/classify", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title: title, description: description }),
  });
  const data = await responce.json();
  console.log(data);
  return data.ministry;
}
export const POST = async (req, res) => {
  const data = await req.json();

  console.log(data);
  const raisedBy = data.id;
  const complaint = data.description;
  const summary = await getSummary(complaint);
  const category = await getMinistry(summary, complaint);
  const tags = "tags";
  const wardno = data.wardno;
  const status = "pending";
  
const date = new Date().toISOString().slice(0, 10);
  
  console.log(raisedBy, complaint, summary, category, tags, wardno, status, date);
  try {
    const complaints = await query({
      query:
        "INSERT INTO complaint (raisedby,complaint,summary,category,tags,wardno,status,date) VALUES (?,?,?,?,?,?,?,?)",
      values: [raisedBy, complaint, summary, category, tags, wardno, status,date],
    });

    if (complaints) {
      return NextResponse.json({ complaints: complaints }, { status: 200 });
    }
  } catch (e) {
    console.log(e.message);
    return NextResponse.json(
      { message: "Error in Inserting Data" },
      { status: 400 }
    );
  }
};

export const GET = async (req, res) => {
  const complaints = await query({
    query: "select * from complaint",
  });

  if (complaints.length > 0) {
    return NextResponse.json({ complaints: complaints }, { status: 200 });
  }
  return NextResponse.json(
    { message: "Cant Fetch complaints" },
    { status: 400 }
  );
};
