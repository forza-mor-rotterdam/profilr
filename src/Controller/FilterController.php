<?php

declare(strict_types=1);

namespace App\Controller;

use Psr\Log\LoggerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\RequestStack;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Contracts\HttpClient\HttpClientInterface;

class FilterController extends AbstractController
{
    #[Route('/filter', name: 'app_filter_index')]
    public function index(Request $request, RequestStack $requestStack, HttpClientInterface $apiClient, LoggerInterface $logger): Response
    {
        // if not logged in, redirect to login page
        if ($requestStack->getSession()->get('is_logged_in') !== true) {
            return $this->redirectToRoute('app_login_index');
        }

        // call api client
        $areas = $apiClient->request('GET', 'https://diensten.rotterdam.nl/sbmob/api/wijken/', [
            'query' => [],
            'auth_bearer' => $requestStack->getSession()->get('msb_token')
        ])->toArray()['result'];

        $incidents = $apiClient->request('POST', 'https://diensten.rotterdam.nl/sbmob/api/msb/openmeldingen', [
            'query' => [],
            'body' => [
                // 'x' => 92441,
                // 'y' => 437718,
                // 'radius' => 200,
                'buurten' => ["24"],
                'wijken' => ["3"]
            ],
            'auth_bearer' => $requestStack->getSession()->get('msb_token')
        ])->toArray()['result'];

        // render template
        return $this->render('filter/index.html.twig', [
            'areas' => $areas
        ]);
    }
}
