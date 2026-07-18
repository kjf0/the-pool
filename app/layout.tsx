import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Poolside — Pool Care Dashboard",
  description: "A calm, practical dashboard for managing home pool chemistry, equipment, and maintenance.",
  icons: { icon: "/favicon.svg", shortcut: "/favicon.svg" },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
