import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "James Fitzgerald — Developer & AI Systems Engineer", description: "Developer portfolio and engineering record for James Fitzgerald and 21amG." };
export default function RootLayout({ children }: Readonly<{children: React.ReactNode}>) { return <html lang="en"><body>{children}</body></html>; }
