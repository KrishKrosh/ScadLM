"use client";

import { Alert, Layout, Select, Space, theme } from 'antd';
import Search from 'antd/es/input/Search';
import { useState } from 'react';
import { getCadDownload as downloadCadFile, getCadShapes as getCadObject, getGeneratedFiles } from './api/cad';
const { Content } = Layout;

const test = true; // Set to true for hardcoded values, false for original fetching

export default function Home() {
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  const [cadShapes, setCadShapes] = useState([]);
  const [isError, setIsError] = useState(false);
  const [cadID, setCadID] = useState<string>();
  const [iterations, setIterations] = useState<string[]>([]);
  const [generatedFiles, setGeneratedFiles] = useState<Record<string, string[]>>({});

  const onSearch = async (value: string) => {
    try {
      setIsError(false);
      if (!test) {
        const cadObject = await getCadObject(value);
        setCadShapes(cadObject.shapes);
        setCadID(cadObject.id);

        // Fetch iterations for the generation
        const iterationDirs = await fetchIterations(cadObject.id);
        setIterations(iterationDirs);

        // Fetch generated files for each iteration
        const filesByIteration: Record<string, string[]> = {};
        for (const iteration of iterationDirs) {
          const files = await getGeneratedFiles(cadObject.id, iteration);
          filesByIteration[iteration] = files;
        }
        setGeneratedFiles(filesByIteration);
      } else {
        // Hardcoded values for testing
        setCadID("20240519094656");
        setIterations(["0", "1"]);
        setGeneratedFiles({
          "0": ["output.png", "output.stl", "output.scad"],
          "1": ["output.png", "output.stl", "output.scad"],
        });
      }

      setIsError(false);
    } catch (error) {
      console.log(error);
      setIsError(true);
    }
  };

  const onDownload = async (file_type: string) => {
    if (cadID && iterations.length > 0) {
      await downloadCadFile(cadID, iterations[0], file_type); // Assuming download from the first iteration
    }
  };

  const fetchIterations = async (generationId: string): Promise<string[]> => {
    const response = await fetch(`${BASE_URL}/models/generated/${generationId}`);
    const data = await response.json();
    return data;
  };

  return (
    <Layout style={{ height: "100vh" }}>
      <Space wrap>
        <Select
          placeholder="Download"
          style={{ width: 120 }}
          onChange={onDownload}
          options={iterations.map(iteration => ({
            value: iteration,
            label: `Iteration ${iteration}`,
          }))}
        />
      </Space>

      <Layout>
        <Layout style={{ padding: '0 24px 24px' }}>
          <Content
            style={{
              margin: 0,
              minHeight: 280,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            {Object.keys(generatedFiles).map(iteration => (
              <div key={iteration} style={{ marginBottom: 20 }}>
                <h3>Iteration {iteration}</h3>
                {generatedFiles[iteration].map(file => (
                  file.endsWith('output.png') && (
                    <img
                      key={file}
                      src={test ? `/20240519094656/${iteration}/${file}` : `${BASE_URL}/generated/${cadID}/${iteration}/${file}`}
                      alt={`Generated output ${file}`}
                      style={{ maxWidth: '100%', display: "block", marginBottom: '10px' }}
                    />
                  )
                ))}
              </div>
            ))}

            {isError && (
              <Space direction="vertical" style={{ width: '100%' }}>
                <Alert
                  message="Error Generating"
                  description="Please try again. To debug check logs and 'generated' directory for latest file"
                  type="error"
                />
              </Space>
            )}

            <Search placeholder="input search text" size="large" onSearch={onSearch} />
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
}
