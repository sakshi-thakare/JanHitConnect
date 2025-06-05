import React from "react";
// import Navbar from "../components/super-admin/navbar";
import Navbar from "@/app/components/super-admin/navbar";
import PredictWater from "@/app/components/super-admin/PredictWater";
export default function page() {
  return (
    <div>
      <Navbar />
      <PredictWater />
    </div>
  );
}
