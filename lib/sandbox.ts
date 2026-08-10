import { Sandbox } from 'e2b-sdk';

export async function createAndRunSandbox(files: { path: string; content: string }[]) {
  const sandbox = await Sandbox.create({
    template: 'nodejs',
  });

  try {
    for (const file of files) {
      await sandbox.filesystem.write(file.path, file.content);
    }

    const hasPackage = files.some(f => f.path === 'package.json');
    if (hasPackage) {
      await sandbox.process.startAndWait('npm install');
    }

    const process = await sandbox.process.start('npm run dev');
    
    return {
      sandboxId: sandbox.id,
      previewUrl: `https://${sandbox.getHost(3000)}`,
      process,
    };
  } catch (error) {
    await sandbox.kill();
    throw error;
  }
}