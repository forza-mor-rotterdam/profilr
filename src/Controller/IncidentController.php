<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\RequestStack;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Contracts\HttpClient\HttpClientInterface;

class IncidentController extends AbstractController
{
    #[Route('/incident', name: 'app_incident_index')]
    public function index(Request $request, RequestStack $requestStack, HttpClientInterface $apiClient): Response
    {
        // if not logged in, redirect to login page
        // if ($requestStack->getSession()->get('is_logged_in') !== true) {
        //     return $this->redirectToRoute('app_login_index');
        // }

        // call api client
        $incidents = $apiClient->request('GET', '/signals/v1/private/signals', [
            'query' => [],
            'auth_bearer' => $requestStack->getSession()->get('msb_token')
        ])->toArray();

        // render template
        return $this->render('incident/index.html.twig', [
            'incidents' => $incidents
        ]);
    }

    #[Route('/incident/{id}', name: 'app_incident_detail')]
    public function detail(Request $request, int $id, RequestStack $requestStack, HttpClientInterface $apiClient): Response
    {
        // if not logged in, redirect to login page
        if ($requestStack->getSession()->get('is_logged_in') !== true) {
            return $this->redirectToRoute('app_login_index');
        }

        // call api client
        $incident = $apiClient->request('GET', '/signals/v1/private/signals/' . $id, [
            'query' => [],
            'auth_bearer' => $requestStack->getSession()->get('msb_token')
        ])->toArray();

        // render template
        return $this->render('incident/detail.html.twig', [
            'id' => $id,
            'incident' => $incident
        ]);
    }
}
