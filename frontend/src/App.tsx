import {BrowserRouter, Routes, Route} from "react-router";

import './App.css'
import LoginPage from "./pages/LoginPage.tsx";
import DashboardPage from "./pages/DashboardPage.tsx";
import ProtectedRoute from "./pages/ProtectedRoute.tsx";
import DashboardLayout from "./components/DashboardLayout.tsx";
import OrganizationPage from "./pages/OrganizationPage.tsx";
import OrganizationDetailsPage from "./pages/OrganizationDetailsPage.tsx";

function App() {

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<LoginPage/>}/>

                <Route
                    element={
                        <ProtectedRoute>
                            <DashboardLayout/>
                        </ProtectedRoute>
                    }
                >
                    <Route
                        path="/dashboard"
                        element={<DashboardPage/>}
                    />
                    <Route
                        path="/organizations"
                        element={<OrganizationPage/>}
                    />
                    <Route
                        path="/organization/:organizationId"
                        element={<OrganizationDetailsPage/>}
                    />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App
