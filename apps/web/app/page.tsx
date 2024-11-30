import { Button } from "@repo/ui/components/ui/button";

export default function Home() {
  return (
    <>
      <h1 className="text-3xl font-bold underline">Hello world!</h1>
      <Button variant={"destructive"} size={"lg"}>
        Hello World
      </Button>
    </>
  );
}
