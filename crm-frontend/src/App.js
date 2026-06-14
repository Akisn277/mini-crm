import React, { useState, useRef } from "react";
import axios from "axios";

const cardStyle = {
  backgroundColor: "white",
  padding: "20px",
  borderRadius: "12px",
  boxShadow: "0px 4px 15px rgba(0,0,0,0.08)",
  textAlign: "center",
};

function App() {
  const [goal, setGoal] = useState("");
  const [campaignData, setCampaignData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [launchResult, setLaunchResult] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [campaigns, setCampaigns] = useState([]);
  const historyRef = useRef(null);


  const launchCampaign = async () => {

  try {

    const response = await axios.post(
      "http://127.0.0.1:5000/campaigns/launch",
      {
        goal
      }
    );

    setLaunchResult(response.data);

  } catch (error) {
    console.log(error);
  }
};
const loadCampaigns = async () => {

  try {

    const response = await axios.get(
      "http://127.0.0.1:5000/campaigns"
    );

    setCampaigns(response.data);

    setTimeout(() => {
      historyRef.current?.scrollIntoView({
        behavior: "smooth"
      });
    }, 100);

  } catch(error) {
    console.log(error);
  }
};
const getAnalytics = async () => {

  try {

    const response = await axios.get(
      `http://127.0.0.1:5000/campaigns/${launchResult.campaign_id}/analytics`
    );

    setAnalytics(response.data);

  } catch(error) {
    console.log(error);
  }
};
  const generateCampaign = async () => {
    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:5000/ai/generate-campaign",
        {
          goal: goal,
        }
      );

      setCampaignData(response.data);
    } catch (error) {
      console.error(error);
      alert("Failed to generate campaign");
    } finally {
      setLoading(false);
    }
  };

 return (
  <div
    style={{
      minHeight: "100vh",
      backgroundColor: "#f8fafc",
      padding: "40px",
      display: "flex",
      justifyContent: "center",
      fontFamily: "Inter, Arial, sans-serif",
    }}
  >
    <div
      style={{
        width: "100%",
        maxWidth: "1200px",
      }}
    >
      <div
        style={{
          background: "linear-gradient(135deg,#2563eb,#7c3aed)",
          color: "white",
          padding: "35px",
          borderRadius: "16px",
          marginBottom: "30px",
        }}
      >
        <h1
          style={{
            margin: 0,
            fontSize: "42px",
          }}
        >
          AI Campaign CRM
        </h1>

        <p
          style={{
            marginTop: "10px",
            opacity: 0.9,
          }}
        >
          Generate, launch and track marketing campaigns using AI
        </p>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: "20px",
          marginBottom: "30px",
        }}
      >
        <div style={cardStyle}>
          <h3>Total Customers</h3>
          <h1>1000</h1>
        </div>

        <div style={cardStyle}>
          <h3>Total Orders</h3>
          <h1>5000</h1>
        </div>

        <div style={cardStyle}>
          <h3>Campaigns</h3>
          <h1>{campaigns.length}</h1>
        </div>

        <div style={cardStyle}>
          <h3>Status</h3>
          <h1>Live</h1>
        </div>
      </div>

      <div
        style={{
          backgroundColor: "white",
          padding: "25px",
          borderRadius: "12px",
          boxShadow: "0px 4px 15px rgba(0,0,0,0.08)",
        }}
      >
        <h3>Campaign Goal</h3>

        <textarea
          rows="5"
          style={{
            width: "100%",
            padding: "15px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
          }}
          placeholder="Example: Re-engage customers who bought Shoes but haven't returned in 90 days"
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
        />

        <br />
        <br />

        <button
          onClick={generateCampaign}
          style={{
            backgroundColor: "#2563eb",
            color: "white",
            border: "none",
            padding: "12px 24px",
            borderRadius: "8px",
            cursor: "pointer",
            fontWeight: "bold",
          }}
        >
          Generate Campaign
        </button>

        <button
          onClick={loadCampaigns}
          style={{
            backgroundColor: "#16a34a",
            color: "white",
            border: "none",
            padding: "12px 24px",
            borderRadius: "8px",
            cursor: "pointer",
            fontWeight: "bold",
            marginLeft: "10px",
          }}
        >
          Campaign History
        </button>
      </div>

      {loading && (
        <h3 style={{ marginTop: "20px" }}>
          Generating Campaign...
        </h3>
      )}

      {campaignData && (
        <div
          style={{
            backgroundColor: "white",
            marginTop: "25px",
            padding: "25px",
            borderRadius: "12px",
            boxShadow: "0px 4px 15px rgba(0,0,0,0.08)",
          }}
        >
          <h2>Campaign Preview</h2>

          <p>
            <strong>Customers Found:</strong>{" "}
            {campaignData.customer_count}
          </p>

          <p>
            <strong>Segment:</strong>{" "}
            {campaignData.campaign.segment_name}
          </p>

          <p>
            <strong>Category:</strong>{" "}
            {campaignData.campaign.category}
          </p>

          <p>
            <strong>Inactive Days:</strong>{" "}
            {campaignData.campaign.inactive_days}
          </p>

          <p>
            <strong>Channel:</strong>{" "}
            {campaignData.campaign.channel}
          </p>

          <h3>Message</h3>

          <div
            style={{
              backgroundColor: "#f1f5f9",
              padding: "15px",
              borderRadius: "8px",
            }}
          >
            {campaignData.campaign.message}
          </div>

          <h3 style={{ marginTop: "25px" }}>
            Sample Customers
          </h3>

          {campaignData.sample_customers.map((customer) => (
            <div
              key={customer.id}
              style={{
                backgroundColor: "#f1f5f9",
                padding: "10px",
                borderRadius: "8px",
                marginBottom: "8px",
              }}
            >
              <strong>{customer.name}</strong>
              <br />
              {customer.email}
            </div>
          ))}

          <button
            onClick={launchCampaign}
            style={{
              backgroundColor: "#2563eb",
              color: "white",
              border: "none",
              padding: "12px 24px",
              borderRadius: "8px",
              cursor: "pointer",
              fontWeight: "bold",
              marginTop: "20px",
            }}
          >
            Launch Campaign
          </button>

          {launchResult && (
            <div
              style={{
                marginTop: "20px",
                backgroundColor: "#dcfce7",
                padding: "15px",
                borderRadius: "8px",
              }}
            >
              <h3>Campaign Launched</h3>

              <p>
                Campaign ID: {launchResult.campaign_id}
              </p>

              <p>
                Customers: {launchResult.customer_count}
              </p>

              <button
                onClick={getAnalytics}
                style={{
                  backgroundColor: "#16a34a",
                  color: "white",
                  border: "none",
                  padding: "10px 20px",
                  borderRadius: "8px",
                  cursor: "pointer",
                  fontWeight: "bold",
                }}
              >
                View Analytics
              </button>
            </div>
          )}

          {analytics && (
            <div style={{ marginTop: "25px" }}>
              <h2>Campaign Analytics</h2>

              <div
                style={{
                  display: "flex",
                  gap: "20px",
                  flexWrap: "wrap",
                }}
              >
                <div
                  style={{
                    backgroundColor: "#dcfce7",
                    padding: "30px",
                    borderRadius: "10px",
                    flex: 1,
                    minWidth: "180px",
                  }}
                >
                  <h3>Delivered</h3>
                  <h1 style={{ fontSize: "36px" }}>{analytics.delivered}</h1>
                </div>

                <div
                  style={{
                    backgroundColor: "#dbeafe",
                    padding: "30px",
                    borderRadius: "10px",
                    flex: 1,
                    minWidth: "180px",
                  }}
                >
                  <h3>Opened</h3>
                  <h1 style={{ fontSize: "36px" }}>{analytics.opened}</h1>
                </div>

                <div
                  style={{
                    backgroundColor: "#ffedd5",
                    padding: "30px",
                    borderRadius: "10px",
                    flex: 1,
                    minWidth: "180px",
                  }}
                >
                  <h3>Clicked</h3>
                  <h1 style={{ fontSize: "36px" }}>{analytics.clicked}</h1>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {campaigns.length > 0 && (
        <div
          ref={historyRef}
          style={{
            backgroundColor: "white",
            marginTop: "25px",
            padding: "25px",
            borderRadius: "12px",
            boxShadow: "0px 4px 15px rgba(0,0,0,0.08)",
          }}
        >
          <h2>Campaign History</h2>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 2fr 1fr 1fr",
              fontWeight: "bold",
              backgroundColor: "#f8fafc",
              padding: "12px",
              borderRadius: "8px",
              marginBottom: "10px",
            }}
          >
            <div>ID</div>
            <div>Segment</div>
            <div>Channel</div>
            <div>Customers</div>
          </div>

          {campaigns.map((campaign) => (
            <div
              key={campaign.id}
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 2fr 1fr 1fr",
                gap: "10px",
                padding: "12px",
                borderBottom: "1px solid #e5e7eb",
              }}
            >
              <div>#{campaign.id}</div>
              <div>{campaign.segment_name}</div>
              <div>{campaign.channel}</div>
              <div>{campaign.customer_count}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  </div>
);
}

export default App;