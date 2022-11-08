<?php

namespace App\Controller;

use Psr\Log\LoggerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\RequestStack;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Contracts\HttpClient\HttpClientInterface;
use Symfony\Contracts\HttpClient\ResponseInterface;

class IncidentController extends AbstractController
{
    #[Route('/incident', name: 'app_incident_index')]
    public function index(Request $request, RequestStack $requestStack, HttpClientInterface $apiClient, LoggerInterface $logger): Response
    {
        // if not logged in, redirect to login page
        if ($requestStack->getSession()->get('is_logged_in') !== true) {
            $logger->warning('Not logged in', ['started' => $requestStack->getSession()->isStarted()]);
            return $this->redirectToRoute('app_login_index');
        }

        // call api client
        $incidents = $apiClient->request('POST', 'https://diensten.rotterdam.nl/sbmob/api/msb/openmeldingen', [
            'query' => [],
            'body' => [
                'x' => 92441,
                'y' => 437718,
                'radius' => 200,
            ],
            'auth_bearer' => $requestStack->getSession()->get('msb_token')
        ])->toArray()['result'];

        $apiCalls = [];
        $i = 0;
        foreach ($incidents as $k => $incident) {
            $i++;
            if ($i > 10) {
                break;
            }
            $apiCalls[$k] = $apiClient->request('GET', 'https://diensten.rotterdam.nl/sbmob/api/msb/melding/' . $incident['id'], [
                'query' => [],
                'auth_bearer' => $requestStack->getSession()->get('msb_token')
            ]);
        }
        foreach ($apiCalls as $k => $apiCall) {
            /** @var ResponseInterface $apiCall */
            $incidents[$k]['_detail'] = $apiCall->toArray()['result'];
        }

        // render template
        return $this->render('incident/index.html.twig', [
            'incidents' => $incidents,
            'controller_name' => "My controller",
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
        $incident = $apiClient->request('GET', 'https://diensten.rotterdam.nl/sbmob/api/msb/melding/' . $id, [
            'query' => [],
            'auth_bearer' => $requestStack->getSession()->get('msb_token')
        ])->toArray()['result'];
        $groupedSubjects = $apiClient->request('GET', 'https://diensten.rotterdam.nl/sbmob/api/msb/onderwerpgroepen/', [
            'query' => [],
            'auth_bearer' => $requestStack->getSession()->get('msb_token')
        ])->toArray()['result'];

        // extend incident with group information
        foreach($groupedSubjects as $group) {
            foreach ($group['onderwerpen'] as $subjects) {
                if ($subjects['code'] == $incident['onderwerp']['id']) {
                    $incident['groep'] = $group;
                    unset($incident['groep']['onderwerpen']);
                    break 2;
                }
            }
        }

        // render template
        return $this->render('incident/detail.html.twig', [
            'id' => $id,
            'incident' => $incident
        ]);
    }

    #[Route('/incident/{id}/handle', name: 'app_incident_handle')]
    public function handle(Request $request, int $id, RequestStack $requestStack, HttpClientInterface $apiClient): Response
    {
        // if not logged in, redirect to login page
        if ($requestStack->getSession()->get('is_logged_in') !== true) {
            return $this->redirectToRoute('app_login_index');
        }

        // call api client
        $incident = $apiClient->request('GET', 'https://diensten.rotterdam.nl/sbmob/api/msb/melding/' . $id, [
            'query' => [],
            'auth_bearer' => $requestStack->getSession()->get('msb_token')
        ])->toArray()['result'];

        $groupedSubjects = $apiClient->request('GET', 'https://diensten.rotterdam.nl/sbmob/api/msb/onderwerpgroepen/', [
            'query' => [],
            'auth_bearer' => $requestStack->getSession()->get('msb_token')
        ])->toArray()['result'];

        // render template
        return $this->render('incident/handle.html.twig', [
            'id' => $id,
            'incident' => $incident,
            'groupedSubjects' => $groupedSubjects
        ]);
    }
}
