"use client";

import { Alert, Layout, Select, Space, theme } from 'antd';
import Search from 'antd/es/input/Search';
import { useState } from 'react';
import { getCadDownload as downloadCadFile, getCadShapes as getCadObject, getGeneratedFiles } from './api/cad';
import CadViewer from './components/cad-viewer';
const { Content } = Layout;

const BASE_URL = "http://127.0.0.1:5001"; // Ensure this URL matches your backend server

export default function Home() {
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  const [cadShapes, setCadShapes] = useState([]);
  const [isError, setIsError] = useState(false);
  const [cadID, setCadID] = useState<string>();
  const [iteration, setIteration] = useState<string>();
  const [generatedFiles, setGeneratedFiles] = useState<string[]>([]);
  const [stlFileUrl, setStlFileUrl] = useState<string>();

  const onSearch = async (value: string) => {
    try {
      setIsError(false);
      const cadObject = await getCadObject(value);
      setCadShapes(cadObject.shapes);
      setCadID(cadObject.id);
      setIteration(cadObject.iteration);
      const files = await getGeneratedFiles(cadObject.id, cadObject.iteration);
      setGeneratedFiles(files);
      setIsError(false);
      const stlFile = files.find(file => file.endsWith('.stl'));
      if (stlFile) {
        setStlFileUrl(`${BASE_URL}/models/generated/${cadObject.id}/${cadObject.iteration}/${stlFile}`);
      }
    } catch {
      console.log("error");
      setIsError(true);
    }
  };

  const onDownload = async (file_type: string) => {
    if (cadID && iteration) {
      await downloadCadFile(cadID, iteration, file_type);
    }
  };

  return (
    <Layout style={{ height: "100vh" }}>
      <Space wrap>
        <Select
          placeholder="Download"
          style={{ width: 120 }}
          onChange={onDownload}
          options={generatedFiles.map(file => ({
            value: file.split('.').pop(),
            label: file,
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
            <Layout>
              <CadViewer cadShapes={cadShapes} stlFileUrl={stlFileUrl} />
            </Layout>
            {generatedFiles.length > 0 && (
              <div style={{ marginTop: 20 }}>
                <h3>Generated Files:</h3>
                <table>
                  <thead>
                    <tr>
                      <th>File Name</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {generatedFiles.map(file => (
                      <tr key={file}>
                        <td>{file}</td>
                        <td>
                          <a
                            href={`${BASE_URL}/models/generated/${cadID}/${iteration}/${file}`}
                            download
                          >
                            Download
                          </a>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </Content>

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
        </Layout>
      </Layout>
    </Layout>
  );
}
